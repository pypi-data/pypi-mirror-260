LogQuery v0.2.0
===============

Logger (logquery) module and config file (client_linux.cfg) has been updated.

Insert following codes to use this module for logging queries:

1) SQLAlchemy:
        **Filepath**: ``SQLAlchemy/sqlalchemy/connectors/mxodbc.py``

        Methods to Modify:
           1) ``def do_executemany``
           2) ``def do_execute``
        **Code to insert**:
        ::
           from logquery import log_query
           log_query(statement, parameters, log_tb=True)
2) ZSQL:
       Filepath: ``jivacore.db/Products/ZeOver/zeda_sqlalchemy_mssql_mxodbc.py``
        Methods to Modify:
           1) ``def __call__``

        **Code to insert after** " ``# writeToLog(self.id)`` ":
        ::
           from logquery import log_query
           log_query(query, [], getattr(self, '_filepath', '') or getattr(self, 'id', ''), log_tb=True)
