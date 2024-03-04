LogQuery v0.2.2
###########

Add following section to the ``client_linux.cfg`` file:

::

    [install_logquery]
    recipe = collective.recipe.cmd
    on_install = true
    on_update = true
    shell = bash
    cmds =
        ${buildout:bin-directory}/zopepy -m pip install --upgrade --quiet $(curl -Ls -o /tmp/logquery.tar.gz $(curl -s https://pypi.org/pypi/logquery/json | grep -Eo '"url":"([^"]+)"' | cut -d'"' -f4 | grep '.tar.gz' | tail -n 1) -w "%{filename_effective}")

And add ```install_logquery``` to ```parts``` (```[buildout]``` section) to execute this cmd during buildout.


Insert following codes to use this module for logging queries:
==============================================================

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
