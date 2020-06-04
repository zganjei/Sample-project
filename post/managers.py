from utils.manager.main import ObjectsManager, ManagerColumn

from .models import Post
from utils.manager.action import EditAction, AddAction, DeleteAction
# from .forms import AccountManagerForm
from .filter_form import PostFilterForm
from .forms import PostForm
# from student.models import WeeklySchedule
# from common.common_functions import start_end_week_date
import datetime


class PostManager(ObjectsManager):
    manager_name = "posts"
    manager_verbose_name = "مدیریت پست ها"
    filter_form = PostFilterForm
    actions = [
        AddAction(PostForm),
        EditAction(PostForm),
        DeleteAction(
            confirm_message='آیا از حذف این پست اطمینان دارید؟'),
    ]

    def __init__(self, http_request, height=None):
        super(PostManager, self).__init__(http_request, height)
        # [start_of_week, end_of_week] = start_end_week_date(datetime.datetime.now())
        # self.weekly_info_obj = WeeklySchedule.objects.filter(start_week_date=start_of_week)

    def get_all_data(self):
        return Post.objects.all()

    def get_columns(self):
        columns = [
            ManagerColumn('title', "عنوان", 5),

        ]
        return columns


    def get_planning(self, obj):
        return "<a href='/student/planning/?userid=%s' target='_blank'>مشاهده</a>" % obj.id

    def get_study(self, obj):
        return "<a href='/student/study-time/?userid=%s' target='_blank'>مشاهده</a>" % obj.id

    def get_testtime(self, obj):
        return "<a href='/student/study-time-test/?userid=%s' target='_blank'>مشاهده</a>" % obj.id

    def get_test(self, obj):
        return "<a href='/student/test-numbers/?userid=%s' target='_blank'>مشاهده</a>" % obj.id

    def get_speedtest(self, obj):
        return "<a href='/student/test-speed/?userid=%s' target='_blank'>مشاهده</a>" % obj.id

    def get_fulltime(self, obj):
        return "<a href='/student/full-study-time/?userid=%s' target='_blank'>مشاهده</a>" % obj.id
