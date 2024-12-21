
class User:
    def __init__(self, user_id, name, age, weight, height):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    def save(self): # save user info to dataset 
         pass

    def fetch(self):
         pass

class Plandesign:
    @staticmethod
    def compute_ffmi(weight, height):
        height_in_meters = height / 100 #ffmi calc
        ffmi = weight / (height_in_meters ** 2)
        return round(ffmi, 2)

    @staticmethod
    def compute_calories(age, weight, height):
        bmr = 10 * weight + 6.25 * height - 5 * age + 5  #calorie calc
        return round(bmr * 1.2) 

    @staticmethod
    def generate_workout_plan():
        return ["Push-ups", "Squats", "cardio"]

    @staticmethod
    def generate_diet_plan():
         return ["Breakfast: Fruits", "Lunch: Pasta", "Dinner: Salad"]



class View:
    @staticmethod
    def display_profile(user):
        print(f"Name: {user.name}, Age: {user.age}, Weight: {user.weight}kg, Height: {user.height}cm")

    @staticmethod
    def display_ffmi(ffmi):
        print(f"Your FFMI: {ffmi}")

    @staticmethod
    def display_calories(calories):
        print(f"Your daily calorie requirement: {calories} kcal")

    @staticmethod
    def display_plan(plan_type, plan):
        print(f"{plan_type} Plan:")
        for item in plan:
            print(f"- {item}")


#login,logout,update info
class UserController:
    def __init__(self):
        self.user = None #initializing user to none

    def login(self, user_id):
        self.user = User(user_id, "Omar", 18, 55, 160)
        print("Login successful")

    def logout(self):
        self.user = None
        print("Logged out")

    def update_profile(self, name=None, age=None, weight=None, height=None):
        if self.user:
            self.user.name = name or self.user.name
            self.user.age = age or self.user.age
            self.user.weight = weight or self.user.weight
            self.user.height = height or self.user.height
            self.user.save()
            print("Profile updated")

class PlanController:
    def __init__(self):
        self.logic = Plandesign()

    def calculate_ffmi(self, user):
        return self.logic.compute_ffmi(user.weight, user.height)

    def calculate_calories(self, user):
        return self.logic.compute_calories(user.age, user.weight, user.height)

    def generate_combined_plan(self):
        workout_plan = self.logic.generate_workout_plan()
        diet_plan = self.logic.generate_diet_plan()
        return workout_plan, diet_plan


#for the site
if __name__ == "__main__":
    user_controller = UserController()
    plan_controller = PlanController()
    view = View()

   
    user_controller.login(user_id=1) #user logging in
    user = user_controller.user
###############
   
    view.display_profile(user)

   ##############
    ffmi = plan_controller.calculate_ffmi(user)
    view.display_ffmi(ffmi)

  #############
    calories = plan_controller.calculate_calories(user)
    view.display_calories(calories)

   #####################
    workout_plan, diet_plan = plan_controller.generate_combined_plan()
    view.display_plan("Workout", workout_plan)
    view.display_plan("Diet", diet_plan)

    user_controller.logout()
