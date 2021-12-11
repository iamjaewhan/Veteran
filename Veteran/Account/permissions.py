from rest_framework import permissions

class IsApproveHostrMakeGameOnly(permissions.BasePermission):
   # 승인된 호스트에 한해 게임 생성 허용
   def has_object_permission(self, request, view, obj):
       # 조회 요청(GET, HEAD, OPTIONS) 에 대해 인증여부 상관없이 허용
       if request.method in permissions.SAFE_METHODS:
          return True
       # PUT, DELETE 요청에 대해 작성자일 경우 요청 허용
       return obj.host == request.user
    