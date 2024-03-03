import argparse

from funread.legado.task import GenerateSourceTask
from funread.legado.task import ReadODSProgressDataTask
from funread.legado.task import ReadODSSourceDataTask
from funread.legado.task import ReadODSUrlDataTask
from funread.legado.task import UpdateRssTask


ReadODSUrlDataTask().run()
ReadODSSourceDataTask().run()
#ReadODSProgressDataTask().run()
#GenerateSourceTask().run()
# GenerateSourceTask().update_rss()
#UpdateRssTask().run()
#UpdateRssTask().update_main()
