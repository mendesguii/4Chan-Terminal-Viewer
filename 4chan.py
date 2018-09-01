from bs4 import BeautifulSoup
import requests
import os
import re

thread_num_c = []

def generate_colors():
    global thread_num_c
    for style in range(8):
        for fg in range(30,38):
            for bg in range(40,48):
                thread_num_c.append('\x1b['+str(style)+';'+str(fg)+';'+str(bg)+'m')
        #print(len(thread_num_c))

def main_page(thread_list,soup,count,forum):
    os.system('clear')
    print('                                   '+'\x1b[1;37;40m'+'\x1b[1;31;40m'+soup.title.text.replace(' - 4chan','')+'\x1b[0m'+' '+'\x1b[0m'+'\n')
    generate_colors()
    for thread in soup.find_all('div',class_='thread'):
            for each_title in thread.find_all('div',class_='post op'):
                title= each_title.find('blockquote',class_='postMessage').text
                number = each_title.find('blockquote',class_='postMessage')['id'].replace('m','')
                if 'The /g/ Wiki' not in title:
                    thread_list.append(number)
                    print('\x1b[1;37;40m'+'======================================= #'+str(count)+' ======================================='+'\x1b[0m')
                    print('                               ||Thread N# '+'\x1b[1;31;40m' +number+'\x1b[0m'+' ||  ')
                    print('\n'+(re.sub("(.{80})", "\\1\n", title.replace('>',''), 0, re.DOTALL)+'\n'))
                    source_thread = requests.get('http://boards.4chan.org/'+forum+'/thread/'+number).text
                    soup_thread = BeautifulSoup(source_thread,"html5lib")
                    count_replies = 0
                    for each_answer in soup_thread.find_all('div',class_='postContainer replyContainer'):
                        count_replies+=1
                    print('- Replies: '+'\x1b[1;31;40m'  +str(count_replies)+'\x1b[0m')
                    count += 1

def fill_array(soup_thread,thread_num):
    for each_answer in soup_thread.find_all('div',class_='postContainer replyContainer'):
            num_thread = each_answer.find('blockquote',class_='postMessage')['id'].replace('m','')
            thread_num.append(num_thread)

def thread_page(query_choice,thread_list,thread_num,forum):
    source_thread = requests.get('http://boards.4chan.org/'+forum+'/thread/'+thread_list[int(query_choice)]).text
    soup_thread = BeautifulSoup(source_thread,"html5lib")
    title_t_page = soup_thread.find('blockquote', class_='postMessage').text
    number_t_page = soup_thread.find('blockquote', class_='postMessage')['id'].replace('m', '')
    os.system('clear')
    print('N# '+number_t_page+' '+'\x1b[1;31;40m' +'OP'+'\x1b[0m'+' '+'\n')
    print(re.sub("(.{80})", "\\1\n", title_t_page, 0, re.DOTALL)) 
    fill_array(soup_thread,thread_num)
    for each_answer in soup_thread.find_all('div',class_='postContainer replyContainer'):            
        answer_text = each_answer.find('blockquote',class_='postMessage').text
        number_answer = each_answer.find('blockquote',class_='postMessage')['id'].replace('m','')

        if number_answer in thread_num:
            number_answer = thread_num_c[thread_num.index(number_answer)]+number_answer+ '\x1b[0m'
        for num in thread_num:
            if num in answer_text:
                answer_text= answer_text.replace(num,thread_num_c[thread_num.index(num)]+num+ '\x1b[0m'+' ')
                #break
        print('\x1b[1;37;40m'+'================================================================================='+'\x1b[0m')
        print('||'+number_answer+'||')  
        print((re.sub("(.{80})", "\\1\n", answer_text.replace(number_t_page,('\x1b[1;31;40m' +'OP'+'\x1b[0m'+' ')).replace('>>','->'), 0, re.DOTALL)))
    #print(list(set(thread_num)))

def only_user_thread(thread,number_user,thread_num,forum):
    source_thread = requests.get('http://boards.4chan.org/'+forum+'/thread/'+thread).text
    soup_thread = BeautifulSoup(source_thread,"html5lib")
    title_t_page = soup_thread.find('blockquote', class_='postMessage').text
    number_t_page = soup_thread.find('blockquote', class_='postMessage')['id'].replace('m', '')
    os.system('clear')
    print('N# '+number_t_page+' '+'\x1b[1;31;40m' +'OP'+'\x1b[0m'+' '+'\n')
    print(title_t_page)
    for each_answer in soup_thread.find_all('div',class_='postContainer replyContainer'):            
        answer_text = each_answer.find('blockquote',class_='postMessage').text
        number_answer = each_answer.find('blockquote',class_='postMessage')['id'].replace('m','')

        if number_answer in thread_num:
            number_answer = thread_num_c[thread_num.index(number_answer)]+number_answer+ '\x1b[0m'
        for num in thread_num:
            if num in answer_text:
                answer_text= answer_text.replace(num,thread_num_c[thread_num.index(num)]+num+ '\x1b[0m'+' ')
                #break
        if (number_user in number_answer or number_user in answer_text):
            print('\x1b[1;37;40m'+'================================================================================='+'\x1b[0m')
            print('||'+number_answer+'||')  
            print((re.sub("(.{80})", "\\1\n", answer_text.replace(number_t_page,('\x1b[1;31;40m' +'OP'+'\x1b[0m'+' ')).replace('>>','->'), 0, re.DOTALL)))   

def main():
    forum = input('Type the forum: ')
    source = requests.get('http://boards.4chan.org/'+forum+'/').text
    soup = BeautifulSoup(source, "html5lib")
    thread_list = []
    thread_num= []
    count = 0
    main_page(thread_list,soup,count,forum)
    #query_choice=input('Choose thread(#): ')
    #thread_page(query_choice,thread_list,thread_num,forum)
    cmd = input('Command: ')
    while(cmd != 'exit'):
        if 'back' in cmd:
            main_page(thread_list,soup,count,forum)
            cmd = input('Command: ')
        if 'change' in cmd:
            main()
        if 'only' in cmd:
            cmd = cmd.split(' ')
            only_user_thread(thread_list[int(aux)],str(cmd[1]),thread_num,forum)
            cmd = input('Command: ')
        if 'back' in cmd:
            thread_page(str(aux),thread_list,thread_num,forum)
            cmd = input('Command: ')
        if 'thread' in cmd:
            cmd = cmd.split(' ')
            aux = cmd[1]
            thread_page(str(cmd[1]),thread_list,thread_num,forum)
            cmd = input('Command: ')
        if 'refresh' in cmd:
            thread_page(str(aux),thread_list,thread_num,forum)
            cmd = input('Command: ')
main()
