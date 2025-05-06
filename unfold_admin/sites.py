from unfold.sites import UnfoldAdminSite


class NewUnfoldAdminSite(UnfoldAdminSite):
    """
    Кастомный админ-сайт, основанный на UnfoldAdminSite.

    Переопределяет заголовки и титулы панели администратора:
    - site_header — отображается в верхней части интерфейса
    - site_title — заголовок страницы (тег <title>)
    - index_title — текст приветствия на главной странице админки
    """
    site_header = 'Unfold Admin Panel'
    site_title = 'Unfold Admin'
    index_title = 'Добро пожаловать в Unfold админку'


unfold_admin_site = NewUnfoldAdminSite(name='unfold_admin')
