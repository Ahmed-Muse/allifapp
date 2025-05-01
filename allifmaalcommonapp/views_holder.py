common_shared_data=[]
request=77
redirect=8
def variables_holder(request):
    allif_data=common_shared_data(request)
    allif_data.get("main_sbscrbr_entity")
    allif_data.get("logged_in_user")
    return redirect('allifmaalcommonapp:commonDivisions',allifusr=allif_data.get("usrslg"),allifslug=allif_data.get("compslg"))