def get_hobbies_prop(hobbies1, hobbies2):
    intersection = hobbies1.intersection(hobbies2)
    union = hobbies1.union(hobbies2)

    print(intersection)
    print(union)
    print()

    prop = int(len(intersection) / len(union) * 100)

    return prop