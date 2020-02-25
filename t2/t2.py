import pprint
import json
import copy


def help_doc(hlp: bool):
    '''
    help function
    '''
    if hlp:
        print('------------------------------------------')
        print("cd - enter in key \n.. - go back \n"
              "ls - show sons \np - show all sons and their values \n")
        print('!!!!!!')
        print("If >>>cd 'key' don't work try: \n>>> ls\n>>> cd (copy key from ls here)")
        print('!!!!!!')
        print()
        print("(keys in dict can be only string)")
        print('------------------------------------------')
    return None


def open_json(path: str):
    """
    open jsop file
    """
    with open(path) as f:
        data = json.load(f)
    return data


def ls_(data):
    '''
    show all sons
    '''
    if type(data) == list:
        for i in range(len(data)):
            print(str(i) + ' - ' + str(type(data[i])))
    elif type(data) == dict:
        for i in data.keys():
            print(str(i) + ' - ' + str(type(data[i])))
    else:
        print('Empty')


def cd_(data, key, pth):
    '''
    go into son
    '''
    new_path = copy.deepcopy(pth)
    if type(data) == list:
        try:
            new_path.append((key, 'list'))
            rez = (data[int(key)], new_path)
            return rez
        except:
            print('Incorrect index')

    elif type(data) == dict:
        try:
            new_path.append((key, 'dict'))
            rez = (data[key], new_path)
            return rez
        except:
            print('Incorrect key')
    else:
        return None


def get_back(data, pth):
    '''
    get back to father
    '''
    new_path = []
    rez_data = copy.deepcopy(data)
    check = 0
    for i in range(len(pth) - 1):
        # print(pth)
        check += 1
        if pth[i][1] == 'dict':
            new_path.append(pth[i])
            rez_data = rez_data[pth[i][0]]
        elif pth[i][1] == 'list':
            new_path.append(pth[i])
            rez_data = rez_data[int(pth[i][0])]
    if check == 0:
        return (rez_data, pth)
    return (rez_data, new_path)


def cmd_live(data):
    '''
    main function
    '''
    live_data = copy.deepcopy(data)
    path = []
    help_doc(True)
    while True:
        comnd = input('>>> ')
        if comnd == 'ls':
            ls_(live_data)

        elif comnd.split()[0] == 'cd':
            rez_cd = cd_(live_data, ' '.join(comnd.split()[1:]), path)
            if rez_cd == None:
                print('No way')
            else:
                live_data = rez_cd[0]
                path = rez_cd[1]

        elif comnd == '..':
            rez_ = get_back(data, path)
            live_data = rez_[0]
            path = rez_[1]

        elif comnd == 'p':
            pp = pprint.PrettyPrinter(indent=4, width=41, compact=True)
            pp.pprint(live_data)

        elif comnd == 'path':
            print(path)

        else:
            print('Input error')


if __name__ == '__main__':
    data = open_json(
        '/home/bogdan/Documents/1yr_2sm_lab/lab_3/t2/json (2).json')
    cmd_live(data)

