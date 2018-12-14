import social_force

if __name__ == "__main__":
    print("The start of the model")
    model_map, exit_list, people_list, wall_list = social_force.create_map_people_wall()
    model = social_force.Model(model_map, exit_list, people_list, wall_list)
    for i in range(20):
        people_list, people_arrive_list = model.update()
        print(people_list.shape)
