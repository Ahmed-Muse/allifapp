common_shared_data=[]
request=77
redirect=8
def variables_holder(request):
    allif_data=common_shared_data(request)
    allif_data=common_shared_data(request)
    obj=[]
    obj.company=allif_data.get("main_sbscrbr_entity")
    obj.division=allif_data.get("logged_user_division")
    obj.branch=allif_data.get("logged_user_branch")
    obj.department=allif_data.get("logged_user_department")
    obj.owner=allif_data.get("usernmeslg")
    #obj.uid=allifuid
    obj.save()
    return redirect('allifmaalcommonapp:commonStocks',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))
