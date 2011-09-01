# -*- coding: utf-8 -*-
import sys
import settings
from django.core.management import setup_environ
setup_environ(settings)
module_name = sys.argv[1]
exec('import %s' % module_name)
exec('%s.%s' % (module_name, ' '.join(sys.argv[2:])))
