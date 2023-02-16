{%- if (cookiecutter.orm == "sa2") %}
#fixme But if you import the models before calling Base.metadata.create_all(), it will work:
# manual add model in here
# fixme from .user import  User
{%- endif %}

{%- if (cookiecutter.orm == "sa2") %}
#fixeme  But if you import the models before calling SqlModel.metadata.create_all(), it will work:
# manual add model in here
# fixme from .user import  User
{%- endif %}
{%- if cookiecutter.orm == "beanie" %}
# todo: beanies register models
# fixme if response id field. you can create the id field with an alias to the _id field e.g
# from beanie.odm.fields import PydanticObjectId
#
# class StudentResponse(BaseModel):
#     id : PydanticObjectId= Field(alias="_id")
{%- endif %}

