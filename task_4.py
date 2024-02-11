comands = {'hello':'hello (cmd)', 
           'add':'create a new contact', 
           'change':'change the contact', 
           'show':'show contacts phone ', 
           'all':'show all contacts', 
           'close': 'close aplication', 
           'exit':'exit'}
Contacts_path = r"source/contacts.txt"
old_dict = {}
contacts_dict = {}

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"
        except Exception as e:
            return f"Error: {e}"

    return inner

@input_error
def promt(msg_promt:str, args=(), msg_err="",ignore_caps=False):
    while True:
        answer=input(msg_promt)
        if ignore_caps: answer=answer.lower()
        if answer and not args or answer in args:
            break
        else: print(msg_err)
    return answer

@input_error
def read_from_file(path:str,dic:dict):
    try:
        with open(path,"r+") as fr:
            for line in fr.readlines():
                contact=line.split()
                dic[contact[0]]=contact[1]
    except Exception as e:
        print(e)
        if save_to_file(path):
            print(f"File {path}\nCreated")
        else: return False
    return True

@input_error
def save_to_file(path:str):
    try:
        with open(path,"w+") as wf:
            wf.writelines(k+" "+ v +"\n" for k,v in contacts_dict.items())
    except Exception as e:
            print(e)
            return False
    return True

@input_error
def add_contact(contact_name:str, contact_phone:str) -> bool:
    if contact_name in contacts_dict:
        return "",""
    else:
        contact_name=contact_name.strip().title()
        contact_phone = contact_phone.strip()
        contacts_dict[contact_name]=contact_phone
        return contact_name, contact_phone

@input_error
def change_contact(contact_name:str, contact_phone:str):
    if contact_name in contacts_dict and promt(f"Change from {contacts_dict[contact_name]} to {contact_phone} Continue? Y/N: ",
                                                  ('Y','y','N','n'),"Enter Y or N").upper()=='Y':
        contacts_dict[contact_name]=contact_phone.strip()
        return contact_name, contact_phone
    else:
        return "",""

@input_error
def show_phone(contact_name:str):
    if contact_name in contacts_dict:
        print(f"{contact_name:25}tel: {contacts_dict[contact_name]:10}")
        return True
    else:
        print("Record not founded!")
        return False

@input_error
def show_all():
    for name, phone in contacts_dict.items():
        print(f"{name:25}tel: {phone:10}")

def main():
    print("\nWelcome to the assistant bot!\n\n        COMMANDS:")
    for command in comands:
        print(f"{command} {"-"*(20-len(command))}{comands[command]}")
    activ = read_from_file(Contacts_path,contacts_dict)
    if activ: old_dict=contacts_dict.copy()
    
    while activ:
        command = promt("Enter command:", tuple(comands.keys()),"Unknown command!",True)
        match command:            
            case "hello": print("\nHow can I help you?\n")
            
            case "add":
                name, phone = add_contact(contact_name=promt(msg_promt="Enter Name: "),
                               contact_phone=promt(msg_promt="Enter Phone: "))
                if name and phone:
                    print(f'Contact added: (Name: {name}-----tel: {phone})')
                else: print(f"Contact not added!")
            
            case "change":
                name, phone = change_contact(contact_name=promt("Enter Name: ", 
                                                                   tuple(contacts_dict.keys()),
                                                                   "Name incorrect!"),
                                             contact_phone=promt(msg_promt="Change Phone: "))
                if phone:
                    print(f'Phone changed: {name}-----tel: {phone}')
                else: print(f"Contact not changed!")            
            
            case "show": 
                show_phone(contact_name=promt("Enter Name: ", tuple(contacts_dict.keys()), "Contact Name not fouded!"))
            
            case "all": show_all()
            
            case "close" | "exit":            
                if contacts_dict!=old_dict and promt("Save to file? (save: Y/N: ",('Y','y','N','n'),"Enter Y or N").upper()=="Y":
                    if save_to_file(Contacts_path): old_dict=contacts_dict.copy()
                print("\nGood bye!\n")
                break

            
            case _: print("Unknown command!\n")
       
if __name__ == "__main__":
    main()
