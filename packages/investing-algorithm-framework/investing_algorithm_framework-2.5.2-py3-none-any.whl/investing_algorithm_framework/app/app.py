import inspect
import logging
import os
import shutil
import threading
from datetime import datetime
from distutils.sysconfig import get_python_lib
from time import sleep

from flask import Flask

from investing_algorithm_framework.app.algorithm import Algorithm
from investing_algorithm_framework.app.stateless import ActionHandler
from investing_algorithm_framework.app.strategy import TradingStrategy
from investing_algorithm_framework.app.task import Task
from investing_algorithm_framework.app.web import create_flask_app
from investing_algorithm_framework.domain import DATABASE_NAME, TimeUnit, \
    DATABASE_DIRECTORY_PATH, RESOURCE_DIRECTORY, ENVIRONMENT, Environment, \
    SQLALCHEMY_DATABASE_URI, OperationalException, BACKTESTING_FLAG, \
    BACKTESTING_START_DATE, BACKTESTING_END_DATE, \
    BACKTESTING_PENDING_ORDER_CHECK_INTERVAL
from investing_algorithm_framework.infrastructure import setup_sqlalchemy, \
    create_all_tables
from investing_algorithm_framework.services import OrderBacktestService, \
    BacktestMarketDataSourceService, BacktestPortfolioService, \
    MarketDataSourceService, MarketCredentialService

logger = logging.getLogger("investing_algorithm_framework")


class App:

    def __init__(self, stateless=False, web=False):
        self._flask_app: Flask = None
        self.container = None
        self._stateless = stateless
        self._web = web
        self.algorithm: Algorithm = None
        self._started = False
        self._strategies = []
        self._tasks = []
        self._configuration_service = None
        self._market_data_source_service: MarketDataSourceService = None
        self._market_credential_service: MarketCredentialService = None

    def set_config(self, config: dict):
        configuration_service = self.container.configuration_service()
        configuration_service.initialize_from_dict(config)

    def initialize_services(self):
        self._configuration_service = self.container.configuration_service()
        self._market_data_source_service = \
            self.container.market_data_source_service()
        self._market_credential_service = \
            self.container.market_credential_service()

    def initialize(self):
        """
        Method to initialize the app. This method should be called before
        running the algorithm. It initializes the services and the algorithm
        and sets up the database if it does not exist.

        :return: None
        """

        if self._web:
            self._initialize_web()
            setup_sqlalchemy(self)
            create_all_tables()
        elif self._stateless:
            self._initialize_stateless()
            setup_sqlalchemy(self)
            create_all_tables()
        else:
            self._initialize_standard()
            setup_sqlalchemy(self)
            create_all_tables()

        # Initialize the algorithm
        self.algorithm = self.container.algorithm()

        # Add strategies
        self.algorithm.add_strategies(self.strategies)

        # Add tasks
        self.algorithm.add_tasks(self.tasks)

        # Initialize all portfolios that are registered
        portfolio_configuration_service = self.container\
            .portfolio_configuration_service()

        # Throw an error if no portfolios are configured
        if portfolio_configuration_service.count() == 0:
            raise OperationalException("No portfolios configured")

        # Create all portfolios
        portfolio_configurations = portfolio_configuration_service.get_all()
        portfolio_service = self.container.portfolio_service()

        for portfolio_configuration in portfolio_configurations:
            # Create portfolio if not exists
            portfolio = portfolio_service.create_portfolio_from_configuration(
                portfolio_configuration
            )
            # Sync all orders from exchange with current order history
            portfolio_service.sync_portfolio_orders(portfolio)

    def _initialize_stateless(self):
        """
        Initialize the app for stateless mode by setting the configuration
        parameters for stateless mode and overriding the services with the
        stateless services equivalents.

        In stateless mode, sqlalchemy is-setup with an in-memory database.

        Stateless has the following implications:
        db: in-memory
        web: False
        app: Run with stateless action objects
        algorithm: Run with stateless action objects
        """
        configuration_service = self.container.configuration_service()
        configuration_service.config[SQLALCHEMY_DATABASE_URI] = "sqlite://"

    def _initialize_standard(self):
        """
        Initialize the app for standard mode by setting the configuration
        parameters for standard mode and overriding the services with the
        standard services equivalents.

        Standard has the following implications:
        db: sqlite
        web: False
        app: Standard
        algorithm: Standard
        """
        configuration_service = self.container.configuration_service()
        resource_dir = configuration_service.config[RESOURCE_DIRECTORY]

        if resource_dir is None:
            configuration_service.config[SQLALCHEMY_DATABASE_URI] = "sqlite://"
        else:
            resource_dir = self._create_resource_directory_if_not_exists()
            configuration_service.config[DATABASE_DIRECTORY_PATH] = \
                os.path.join(resource_dir, "databases")
            configuration_service.config[DATABASE_NAME] \
                = "prod-database.sqlite3"
            configuration_service.config[SQLALCHEMY_DATABASE_URI] = \
                "sqlite:///" + os.path.join(
                    configuration_service.config[DATABASE_DIRECTORY_PATH],
                    configuration_service.config[DATABASE_NAME]
                )
            self._create_database_if_not_exists()

    def _initialize_backtest(
        self,
        backtest_start_date,
        backtest_end_date,
        pending_order_check_interval
    ) -> None:
        """
        Initialize the app for backtesting by setting the configuration
        parameters for backtesting and overriding the services with the
        backtest services equivalents. This method should only be called
        when running a backtest.

        :param backtest_start_date: The start date of the backtest
        :return: None
        """
        configuration_service = self.container.configuration_service()
        resource_dir = configuration_service.config[RESOURCE_DIRECTORY]
        configuration_service.config[BACKTESTING_FLAG] = True
        configuration_service.config[BACKTESTING_START_DATE] = \
            backtest_start_date
        configuration_service.config[BACKTESTING_END_DATE] = backtest_end_date
        configuration_service.config[BACKTESTING_PENDING_ORDER_CHECK_INTERVAL]\
            = pending_order_check_interval

        if resource_dir is None:
            raise OperationalException(
                "Resource directory is not specified. "
                "A resource directory is required for running a backtest."
            )

        resource_dir = self._create_resource_directory_if_not_exists()
        configuration_service.config[DATABASE_DIRECTORY_PATH] = \
            os.path.join(resource_dir, "databases")
        configuration_service.config[DATABASE_NAME] = \
            "backtest-database.sqlite3"
        database_path = os.path.join(
            configuration_service.config[DATABASE_DIRECTORY_PATH],
            configuration_service.config[DATABASE_NAME]
        )

        if os.path.exists(database_path):
            os.remove(database_path)

        configuration_service.config[SQLALCHEMY_DATABASE_URI] = \
            "sqlite:///" + os.path.join(
                configuration_service.config[DATABASE_DIRECTORY_PATH],
                configuration_service.config[DATABASE_NAME]
            )
        self._create_database_if_not_exists()
        setup_sqlalchemy(self)
        create_all_tables()

        # Override the MarketDataSourceService service with the backtest
        # market data source service equivalent. Additionally, convert the
        # market data sources to backtest market data sources
        # market_data_sources = self.get_market_data_sources()
        # backtest_market_data_sources = []
        market_data_sources_service: MarketDataSourceService = \
            self.container.market_data_source_service()
        market_data_sources = market_data_sources_service\
            .get_market_data_sources()
        backtest_market_data_sources = [
            market_data_source.to_backtest_market_data_source()
            for market_data_source in market_data_sources
        ]
        self.container.market_data_source_service.override(
            BacktestMarketDataSourceService(
                market_data_sources=backtest_market_data_sources,
                market_service=self.container.market_service(),
                market_credential_service=self.container
                .market_credential_service(),
                configuration_service=self.container.configuration_service(),
            )
        )
        # Override the portfolio service with the backtest portfolio service
        self.container.portfolio_service.override(BacktestPortfolioService(
            market_service=self.container.market_service(),
            position_repository=self.container.position_repository(),
            order_service=self.container.order_service(),
            portfolio_repository=self.container.portfolio_repository(),
            portfolio_configuration_service=self.container
            .portfolio_configuration_service(),
            portfolio_snapshot_service=self.container
            .portfolio_snapshot_service(),
        ))
        market_data_source_service = \
            self.container.market_data_source_service()

        # Override the order service with the backtest order service
        self.container.order_service.override(
            OrderBacktestService(
                order_repository=self.container.order_repository(),
                order_fee_repository=self.container.order_fee_repository(),
                position_repository=self.container.position_repository(),
                portfolio_repository=self.container.portfolio_repository(),
                portfolio_configuration_service=self.container
                .portfolio_configuration_service(),
                portfolio_snapshot_service=self.container
                .portfolio_snapshot_service(),
                configuration_service=self.container.configuration_service(),
                market_data_source_service=market_data_source_service
            )
        )

        portfolio_configuration_service = self.container \
            .portfolio_configuration_service()

        # Re-init the market service because the portfolio configuration
        # service is a singleton
        portfolio_configuration_service.market_service \
            = self.container.market_service()

        if portfolio_configuration_service.count() == 0:
            raise OperationalException("No portfolios configured")

        # Create all portfolios
        portfolio_configurations = portfolio_configuration_service.get_all()
        portfolio_service = self.container.portfolio_service()

        for portfolio_configuration in portfolio_configurations:
            portfolio_service.create_portfolio_from_configuration(
                portfolio_configuration
            )

        self.algorithm = self.container.algorithm()
        self.algorithm.add_strategies(self.strategies)

    def _initialize_management_commands(self):

        if not Environment.TEST.equals(self.config.get(ENVIRONMENT)):
            # Copy the template manage.py file to the resource directory of the
            # algorithm
            management_commands_template = os.path.join(
                get_python_lib(),
                "investing_algorithm_framework/templates/manage.py"
            )
            destination = os.path.join(
                self.config.get(RESOURCE_DIRECTORY), "manage.py"
            )

            if not os.path.exists(destination):
                shutil.copy(management_commands_template, destination)

    def run(
        self,
        payload: dict = None,
        number_of_iterations: int = None,
    ):
        self.initialize()
        self.algorithm.start(
            number_of_iterations=number_of_iterations,
            stateless=self.stateless
        )

        if self.stateless:
            logger.info("Running stateless")
            action_handler = ActionHandler.of(payload)
            return action_handler.handle(
                payload=payload, algorithm=self.algorithm
            )
        elif self._web:
            logger.info("Running web")
            flask_thread = threading.Thread(
                name='Web App',
                target=self._flask_app.run,
                kwargs={"port": 8080}
            )
            flask_thread.setDaemon(True)
            flask_thread.start()

        number_of_iterations_since_last_orders_check = 1
        self.algorithm.check_pending_orders()

        try:
            while self.algorithm.running:
                if number_of_iterations_since_last_orders_check == 30:
                    logger.info("Checking pending orders")
                    self.algorithm.check_pending_orders()
                    number_of_iterations_since_last_orders_check = 1

                self.algorithm.run_jobs()
                number_of_iterations_since_last_orders_check += 1
                sleep(1)
        except KeyboardInterrupt:
            exit(0)

    def start_algorithm(self):
        self.algorithm.start()

    def stop_algorithm(self):

        if self.algorithm.running:
            self.algorithm.stop()

    @property
    def started(self):
        return self._started

    @property
    def config(self):
        configuration_service = self.container.configuration_service()
        return configuration_service.config

    @config.setter
    def config(self, config: dict):
        configuration_service = self.container.configuration_service()
        configuration_service.initialize_from_dict(config)

    def reset(self):
        self._started = False
        self.algorithm.reset()

    def add_portfolio_configuration(self, portfolio_configuration):
        portfolio_configuration_service = self.container\
            .portfolio_configuration_service()
        portfolio_configuration_service.add(portfolio_configuration)

    @property
    def stateless(self):
        return self._stateless

    @property
    def web(self):
        return self._web

    @property
    def running(self):
        return self.algorithm.running

    def task(
        self,
        function=None,
        time_unit: TimeUnit = TimeUnit.MINUTE,
        interval=10,
    ):
        if function:
            task = Task(
                decorated=function,
                time_unit=time_unit,
                interval=interval,
            )
            self.add_task(task)
        else:
            def wrapper(f):
                self.add_task(
                    Task(
                        decorated=f,
                        time_unit=time_unit,
                        interval=interval
                    )
                )
                return f

            return wrapper

    def strategy(
        self,
        function=None,
        time_unit: TimeUnit = TimeUnit.MINUTE,
        interval=10,
        market_data_sources=None,
    ):

        if function:
            strategy_object = TradingStrategy(
                decorated=function,
                time_unit=time_unit,
                interval=interval,
                market_data_sources=market_data_sources
            )
            self.add_strategy(strategy_object)
        else:

            def wrapper(f):
                self.add_strategy(
                    TradingStrategy(
                        decorated=f,
                        time_unit=time_unit,
                        interval=interval,
                        market_data_sources=market_data_sources,
                        worker_id=f.__name__
                    )
                )
                return f

            return wrapper

    def add_strategies(self, strategies):

        for strategy in strategies:
            self.add_strategy(strategy)

    def add_strategy(self, strategy):

        if inspect.isclass(strategy):
            strategy = strategy()

        assert isinstance(strategy, TradingStrategy), \
            OperationalException(
                "Strategy object is not an instance of a Strategy"
            )

        self._strategies.append(strategy)

    def add_task(self, task):
        if inspect.isclass(task):
            task = task()

        assert isinstance(task, Task), \
            OperationalException(
                "Task object is not an instance of a Task"
            )

        self._tasks.append(task)

    @property
    def strategies(self):
        return self._strategies

    @property
    def tasks(self):
        return self._tasks

    def _initialize_web(self):
        configuration_service = self.container.configuration_service()
        resource_dir = configuration_service.config[RESOURCE_DIRECTORY]

        if resource_dir is None:
            configuration_service.config[SQLALCHEMY_DATABASE_URI] = "sqlite://"
        else:
            resource_dir = self._create_resource_directory_if_not_exists()
            configuration_service.config[DATABASE_DIRECTORY_PATH] = \
                os.path.join(resource_dir, "databases")
            configuration_service.config[DATABASE_NAME] \
                = "prod-database.sqlite3"
            configuration_service.config[SQLALCHEMY_DATABASE_URI] = \
                "sqlite:///" + os.path.join(
                    configuration_service.config[DATABASE_DIRECTORY_PATH],
                    configuration_service.config[DATABASE_NAME]
                )
            self._create_database_if_not_exists()

        self._flask_app = create_flask_app(configuration_service.config)

    def _create_resource_directory_if_not_exists(self):

        if self._stateless:
            return

        configuration_service = self.container.configuration_service()
        resource_dir = configuration_service.config.get(
            RESOURCE_DIRECTORY, None
        )

        if resource_dir is None:
            return

        if not os.path.exists(resource_dir):
            try:
                os.makedirs(resource_dir)
                open(resource_dir, 'w').close()
            except OSError as e:
                logger.error(e)
                raise OperationalException(
                    "Could not create resource directory"
                )

        return resource_dir

    def _create_database_if_not_exists(self):

        if self._stateless:
            return

        configuration_service = self.container.configuration_service()
        database_dir = configuration_service.config\
            .get(DATABASE_DIRECTORY_PATH, None)

        if database_dir is None:
            return

        database_name = configuration_service.config.get(DATABASE_NAME, None)

        if database_name is None:
            return

        database_path = os.path.join(database_dir, database_name)

        if not os.path.exists(database_path):

            if not os.path.isdir(database_dir):
                os.makedirs(database_dir)

            try:
                open(database_path, 'w').close()
            except OSError as e:
                logger.error(e)
                raise OperationalException(
                    "Could not create database directory"
                )

    def get_portfolio_configurations(self):
        return self.algorithm.get_portfolio_configurations()

    def backtest(
        self,
        start_date,
        end_date,
        pending_order_check_interval='1h',
        output_directory=None
    ):
        logger.info("Initializing backtest")

        if end_date is None:
            end_date = datetime.utcnow()

        self._initialize_backtest(
            backtest_start_date=start_date,
            backtest_end_date=end_date,
            pending_order_check_interval=pending_order_check_interval
        )
        backtest_service = self.container.backtest_service()
        backtest_service.resource_directory = self.config.get(
            RESOURCE_DIRECTORY
        )
        report = backtest_service.backtest(
            self.algorithm, start_date, end_date
        )
        backtest_report_writer_service = self.container\
            .backtest_report_writer_service()

        if output_directory is None:
            output_directory = os.path.join(
                self.config.get(RESOURCE_DIRECTORY),
                "backtest_reports"
            )

        backtest_report_writer_service.write_report_to_csv(
            report=report, output_directory=output_directory
        )

        return report

    def add_market_data_source(self, market_data_source):
        self._market_data_source_service.add(market_data_source)

    def add_market_credential(self, market_credential):
        self._market_credential_service.add(market_credential)
