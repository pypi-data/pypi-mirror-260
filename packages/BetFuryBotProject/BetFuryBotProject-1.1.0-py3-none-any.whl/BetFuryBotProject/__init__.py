import os
from brw_run import brw_run, regexp, new_wallets, urljoin
from excel import excel_open, excel_sheet, excel_sheets_rows
from multiprocessing import Pool

def create_new_wallets():
    b_add_wallets = 'y'
    root_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = urljoin(root_dir, r'Sid_Phrases\sides')
    book = excel_open(excel_path)
    sheet = excel_sheet(book)
    rn = excel_sheets_rows(sheet, 1)
    new_wallets(b_add_wallets, rn, excel_path)

if __name__ == '__main__':
    #b_add_wallets = regexp(r'^[yn]$', 'Do You want add wallets?(y/n) ')
    if regexp(r'^[yn]$', 'Do You want add wallets?(y/n) ') == 'y':
        create_new_wallets()
    process_count = int(regexp(r'^\d+$', 'Enter the number of profiles: '))
    #url = input("Enter the URL: ")
    #urls_list = [url] * process_count
    #print(urls_list)
    process_count_list = []
    for i in range(process_count):
        process_count_list.append(str(i+1))
    p = Pool(processes=process_count)
    p.map(brw_run, process_count_list)