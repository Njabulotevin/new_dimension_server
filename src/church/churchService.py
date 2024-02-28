from .churchDAO import ChurchDAO

def church_name_exist(church_name : str, churchDAO : ChurchDAO):
    try:
        church = churchDAO.find_by_query({"name" : church_name})
        print("church found!: ", church)
        return church
    except Exception as e:
        print(e)
        return None