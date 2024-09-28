class User:
    def __init__(self, diet_type, allergies):
        # 사용자 식단 유형과 알레르기 정보 저장
        self.diet_type = diet_type
        self.allergies = allergies

    def get_user_info(self):
        # 사용자 정보 반환
        return {
            "diet_type": self.diet_type,
            "allergies": self.allergies
        }


class Ingredient:
    def __init__(self, name):
        # 재료 이름 저장
        self.name = name

    def get_substitutes(self):
        # 하드코딩된 대체 재료 반환 (고기 및 소시지 포함)
        substitutes = {
            "달걀": ["두부", "아보카도"],
            "우유": ["아몬드 밀크", "두유"],
            "밀": ["퀴노아", "현미"],
            "콩": ["렌틸콩", "병아리콩"],
            "땅콩": ["해바라기씨", "캐슈너트"],
            "밤": ["호두", "캐슈너트"],
            "생선": ["두부", "버섯"],
            "조개": ["버섯", "감자"],
            "소고기": ["두부", "세이탄(밀 글루텐)"],
            "돼지고기": ["템페(콩 발효 식품)", "버섯"],
            "닭고기": ["두부", "콜리플라워"],
            "소시지": ["비건 소시지", "채식용 소시지"],
        }
        return substitutes.get(self.name, [])


class Recipe:
    def __init__(self, title, ingredients):
        # 레시피 제목과 재료 목록 저장
        self.title = title
        self.ingredients = ingredients

    def get_recipe_details(self):
        # 레시피의 제목과 재료를 반환
        return {
            "title": self.title,
            "ingredients": self.ingredients
        }


class SubstituteFinder:
    def __init__(self):
        pass

    def find_substitutes(self, ingredient_name):
        # 재료 이름을 받아 해당 재료의 대체품 찾기
        ingredient = Ingredient(ingredient_name)
        return ingredient.get_substitutes()


class RecipeTransformer:
    def __init__(self, user):
        # 사용자 정보 저장 (식단 유형 및 알레르기 정보)
        self.user = user

    def transform_recipe(self, recipe):
        # 사용자가 식단 제한이나 알레르기가 없는 경우 레시피 그대로 출력
        if self.user.diet_type == "없음" and not self.user.allergies:
            print("제한 사항이 없으므로 레시피가 그대로 출력됩니다.")
            return recipe

        # 재료 목록을 변환하는 함수
        transformed_ingredients = []
        for ingredient in recipe.ingredients:
            original_ingredient = ingredient.strip()  # 재료 이름의 공백 제거
            replaced = False  # 대체가 되었는지 여부를 저장하는 플래그

            # 채식주의자 식단을 고려해 고기 및 소시지 대체
            if "채식주의자" in self.user.diet_type and original_ingredient in ["소고기", "돼지고기", "닭고기", "소시지"]:
                print(f"{original_ingredient}은(는) 채식주의자 식단에 맞지 않습니다.")
                substitutes = SubstituteFinder().find_substitutes(original_ingredient)
                if substitutes:
                    print(f"{original_ingredient}을(를) 대체할 수 있는 재료: {', '.join(substitutes)}")
                    chosen_substitute = input(f"{original_ingredient} 대신 어떤 재료를 사용할까요? ")
                    if chosen_substitute in substitutes:
                        transformed_ingredients.append(f"{original_ingredient} -> {chosen_substitute}")
                        replaced = True  # 대체되었음을 기록
                    else:
                        print("유효한 대체 재료가 아닙니다.")
                        return None
                else:
                    return None

            # 알레르기 재료 대체 처리
            elif original_ingredient in self.user.allergies:
                print(f"{original_ingredient}는 알레르기 정보에 포함되어 있습니다.")
                substitutes = SubstituteFinder().find_substitutes(original_ingredient)
                if substitutes:
                    print(f"{original_ingredient}을(를) 대체할 수 있는 재료: {', '.join(substitutes)}")
                    chosen_substitute = input(f"{original_ingredient} 대신 어떤 재료를 사용할까요? ")
                    if chosen_substitute in substitutes:
                        transformed_ingredients.append(f"{original_ingredient} -> {chosen_substitute}")
                        replaced = True  # 대체되었음을 기록
                    else:
                        print("유효한 대체 재료가 아닙니다.")
                        return None
                else:
                    return None

            # 대체되지 않은 재료는 그대로 추가
            if not replaced:
                transformed_ingredients.append(original_ingredient)

        # 변환된 재료로 새로운 레시피 객체 생성
        transformed_recipe = Recipe(recipe.title + " (변환됨)", transformed_ingredients)
        return transformed_recipe

    def generate_instructions(self, recipe):
        # 레시피 제목에 따라 맞춤형 조리법 생성
        instructions = "재료들을 적절히 준비한 뒤 조리해주세요!"
        if "볶음밥" in recipe.title:
            instructions = "모든 재료를 기름에 볶아주세요!"
        elif "스프" in recipe.title:
            instructions = "모든 재료를 물에 넣고 끓여주세요!"
        elif "샐러드" in recipe.title:
            instructions = "모든 재료를 신선하게 섞어주세요!"
        return instructions


# 사용 예시
if __name__ == "__main__":
    # 사용자로부터 식단 유형 및 알레르기 정보 입력받기
    diet_type = input("당신의 식단 유형을 입력하세요 (없음 입력 시 제한 사항 없음): ")
    allergies = input("당신의 알레르기를 입력하세요 (없음 입력 시 제한 사항 없음): ").split(",")

    # 알레르기가 '없음'이라면 빈 리스트로 처리
    if "없음" in allergies:
        allergies = []

    # User 객체 생성
    user = User(diet_type=diet_type.strip(), allergies=[a.strip() for a in allergies])

    # 기존 레시피 제목 및 재료 입력받기
    original_recipe_title = input("변환할 레시피 제목을 입력하세요: ")
    original_ingredients = input("레시피 재료를 입력하세요 (쉼표로 구분): ").split(",")

    # 입력된 정보를 바탕으로 Recipe 객체 생성
    original_recipe = Recipe(original_recipe_title, [i.strip() for i in original_ingredients])

    # 레시피 변환 진행
    transformer = RecipeTransformer(user)
    transformed_recipe = transformer.transform_recipe(original_recipe)

    if transformed_recipe:
        # 변환된 재료 및 레시피 출력
        print("변환된 재료:")
        for ingredient in transformed_recipe.ingredients:
            print(f"- {ingredient}")

        # 조리법 생성 및 출력
        instructions = transformer.generate_instructions(transformed_recipe)
        print("조리법:")
        print(instructions)
    else:
        print("레시피 변환에 실패했습니다.")
