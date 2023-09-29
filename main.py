import subprocess
import csv
from bs4 import BeautifulSoup

def fetch_sisben(cedula: str):
  curl_command = [
    'curl',
    '-k',
    'https://reportes.sisben.gov.co/dnp_sisbenconsulta',
    '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    '-H', 'Accept-Language: es-ES,es;q=0.9',
    '-H', 'Cache-Control: max-age=0',
    '-H', 'Connection: keep-alive',
    '-H', 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryoBhA081LFIE0IRlg',
    '-H', 'Cookie: .AspNetCore.Antiforgery.GjmQz4LteYk=CfDJ8Hs78MvEfs1NmaTTV6uXoZ8Qh-0Nh7ot1RI7KUPMD3hK-Pfe_hmpYU8GLZJ_Pfb2bpkiqjkih96SyVN3IdGi4qpeXcL7pgaThrUqhQtL8vHFMjMd4LecRpfIUBgM8Hc3aDFUtjoFJ3JlBDCt4mhqVZI; _ga=GA1.3.53468749.1695869381; _gid=GA1.3.865669785.1695869381; _ga_HMFX23YB4K=GS1.1.1695869381.1.0.1695869382.0.0.0',
    '-H', 'Origin: https://reportes.sisben.gov.co',
    '-H', 'Referer: https://reportes.sisben.gov.co/dnp_sisbenconsulta',
    '-H', 'Sec-Fetch-Dest: iframe',
    '-H', 'Sec-Fetch-Mode: navigate',
    '-H', 'Sec-Fetch-Site: same-origin',
    '-H', 'Sec-Fetch-User: ?1',
    '-H', 'Upgrade-Insecure-Requests: 1',
    '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    '-H', 'sec-ch-ua: "Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    '-H', 'sec-ch-ua-mobile: ?0',
    '-H', 'sec-ch-ua-platform: "Windows"',
    '--data-raw', f'------WebKitFormBoundaryoBhA081LFIE0IRlg\r\nContent-Disposition: form-data; name="TipoID"\r\n\r\n3\r\n------WebKitFormBoundaryoBhA081LFIE0IRlg\r\nContent-Disposition: form-data; name="documento"\r\n\r\n{cedula}\r\n------WebKitFormBoundaryoBhA081LFIE0IRlg\r\nContent-Disposition: form-data; name="__RequestVerificationToken"\r\n\r\nCfDJ8Hs78MvEfs1NmaTTV6uXoZ_3qkr537dR5e0iLu4Zl07ftQGuvjL3I_pz5ta_XzkRnmEe_FokTCljQtfARn7K2JECRc8zJy0p_JMFBsL5e7MJvwKcNH4_zfuWzxLUTAonIXXIPOmWNhYyr13u5qZEaBY\r\n------WebKitFormBoundaryoBhA081LFIE0IRlg--\r\n',
    '--compressed'
  ]

  result = subprocess.run(curl_command, capture_output=True, text=True)

  if result.returncode == 0:
    soup = BeautifulSoup(result.stdout, 'html.parser')

    divs_containing_municipio = soup.find_all('p', string='Municipio:')

    if divs_containing_municipio:
        return divs_containing_municipio[0].find_next_sibling().text.strip()
    else:
        return "NA"
  else:
    print(result.stderr)
    return "ERROR"

def generate_file(
    file_name_original,
    file_name_save, 
    cedula_column_index, 
    column_to_write_index=-1
):
  with open(f'/content/{file_name_original}.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    with open(f'/content/{file_name_save}.csv', mode='w', newline='') as updated_csv_file:
      csv_writer = csv.writer(updated_csv_file, delimiter=',')
      header = next(csv_reader)
      csv_writer.writerow(header)
      for row in csv_reader:
        cedula_to_search = row[cedula_column_index-1]
        municipio = fetch_sisben(cedula_to_search)
        if column_to_write_index == -1:
          row.append(municipio)
        else:
          row[column_to_write_index-1] = municipio
        csv_writer.writerow(row)

generate_file(
    file_name_original="conversor",
    file_name_save="final", 
    cedula_column_index=5, 
    column_to_write_index=12
)
