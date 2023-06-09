import os.path

from mako.template import Template

template_dir = os.path.dirname(__file__)
base_template = Template(filename=f"{template_dir}/base.py.mako")
spark_template = Template(filename=f"{template_dir}/spark.py.mako")
elasticsearch_template = Template(filename=f"{template_dir}/elasticsearch.py.mako")
sqlalchemy_template = Template(filename=f"{template_dir}/sqlalchemy.py.mako")
