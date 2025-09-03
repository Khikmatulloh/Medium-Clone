from starlette_admin.contrib.sqla import Admin
from app.admin.views import UserAdminView, ArticleAdminView
from app.database import engine
from app.models import User, Article
from app.admin.auth import AdminAuth

admin = Admin(
    engine=engine,
    title="Bookla Admin",
    base_url="/admin",
    auth_provider=AdminAuth(),  # 🔑 faqat adminlar kira oladi
)

# Admin panelga viewlar qo‘shish
admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(ArticleAdminView(Article, icon="fa fa-book"))

