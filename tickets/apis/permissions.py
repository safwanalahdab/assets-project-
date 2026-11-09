def is_staff(user) : 
    return bool(
        user and 
        user.is_authenticated and 
        getattr(getattr(user, 'profile', None), 'is_staff', False)
    )


                        
