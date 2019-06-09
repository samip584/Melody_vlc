import json



def main():
    while True:
        choice=input("enter choice\n1)add data\n2)show all data\n3)")
        if choice == '1':
            add_data()
        if choice == '2':
            show_all_data()
        if choice == '3':
            exit()



def add_data():
    name = input("enter name ")
    preset = input("enter preset ")

    try:
        with open("equi.txt", "r") as file:
            music_data = json.load(file)

    except:
        music_data = []

    music_data.append({"Name" : name, "Preset": preset})

    with open("equi.txt","w") as file:
        json.dump(music_data, file)


    file.close()

def show_all_data():
    with open("equi.txt","r") as file:
        music_data = json.load(file)

    for student in music_data:
        print(student["Name"], student["Preset"])





if __name__ == "__main__":
    main()