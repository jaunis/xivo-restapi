#!/bin/sh
PYTHONPATH=..:../../xivo_restapi:../../../xivo-dao/xivo-dao:../../../xivo-lib-python/xivo-lib-python lettuce features/users_services.feature --with-xunit --verbosity=3 --xunit-file=xunit-tests-agent.xml
