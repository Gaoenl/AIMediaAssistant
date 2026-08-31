from app.models.factory import create_provider

# 进程内单例,业务代码统一从这里取
provider = create_provider()