from os import system


def clear_console():
    system('clear')
    return

def main():
    clear_console()
    while True:
        # 开始询问所需功能
        print('==========本地自签证书系统==========')
        print('使用前必须先安装 openssl3 系统库!')
        print('请选择功能')
        print('1. 初始化目录内容(在新目录使用时必须执行)')
        print('2. 新建CA证书')
        print('3. 自签名SSL证书')
        print('8. 检查openssl版本')
        print('9. 手动模式(正在开发)')
        print('0. 退出')
        print('----------------------------------')
        choise: str = input('请输入您想要使用的功能: ')
        # --EndRegion--

        # 根据选择的功能确定模块
        if choise == '0': # 退出
            break

        if choise == '1': # 初始化目录
            init_path()
            clear_console()
            print('目录已初始化！\n')
        
        if choise == '2': # 生成新CA
            clear_console()
            print('==========生成新CA证书==========')
            generate_ca(ca_info=get_info())
            clear_console()
            print('已生成新CA机构与证书!\n')

        if choise == '3':
            clear_console()
            print('==========生成新SSL证书=========')
            print('使用前必须生成过CA证书')
            print('(不必每次都使用新CA证书)')
            use_added_key = input('是否需要导入私钥?(y/N): ')
            ssl_name: str = input('请输入您的SSL文件名(不需要输入后缀名!): ')
            print('备注: 将在程序运行目录下生成SSL文件')
            print(f'若您导入私钥, 请命名为{ssl_name}.key')
            ssl_time: str = input('请输入此SSL证书的有效时长: ')
            if use_added_key == 'y' or use_added_key == 'Y':
                generate_ssl(ssl_name, info=get_info(), time=int(ssl_time), use_added_keys=True)
            if use_added_key == 'n' or use_added_key == 'N':
                generate_ssl(ssl_name, info=get_info(), time=int(ssl_time), use_added_keys=False)
            else:
                print('配置出错, 请重试')
            clear_console()
            print('已生成新SSL证书!\n')

        if choise == '8': # 输出openssl版本
            clear_console()
            print('正在检查openssl系统版本……需要您人工查看')
            system('openssl --version')
            print('若出现"command not found"等字样,则表示未安装')
            print('若未安装,请您自行上网搜索教程!')
            print('')
    return


def get_info(): # 模块：请求输入证书信息
    a: str = input('是否使用默认配置?(y/N): ')
    if a == 'y':
        return '"/C=CN/L=Default City/CN=Self-Signed Root CA"'
    else:
        print('---------开始配置证书机构信息---------')
        C: str = input('请输入国家: ')
        ST: str = input('请输入省份: ')
        L: str = input('请输入城市: ')
        O: str = input('请输入组织名: ')
        OU: str = input('[可选]请输入组织内部机构名称: ')
        CN: str = input('[可选]请输入证书“常用名”(显示名称): ')
        info: str = f"/C={C}/ST={ST}/L={L}/O={O}/OU={OU}/CN={CN}"
        return info


def generate_ca(ca_info: str = '"/C=CN/L=Default City/CN=Self-Signed Root CA"', time: int = 3650): # 模块：生成CA证书
    workpath: str = './ca'
    generate_private_key(workpath+'/privatekey.key')
    system(f'openssl req -new -sha256 -x509 -days {time} -key {workpath}/privatekey.key -subj {ca_info} -out {workpath}/cert.crt')
    return


def generate_ssl(ssl_name: str, info: str = '"/C=CN/L=Default City/CN=Self-Signed Cert"',ca_cert_path:str = 'ca/cert.crt', ca_key_path:str = 'ca/privatekey.key', time: int = 90, use_added_keys: bool = False):
    workpath: str = '.'

    private_key_path: str = f'{workpath}/{ssl_name}.key'
    csr_path: str = f'{workpath}/{ssl_name}.csr'
    cert_path: str = f'{workpath}/{ssl_name}.crt'

    make_config()

    if not use_added_keys:
        generate_private_key(private_key_path)
    system(f'openssl req -new -sha256 -key {private_key_path} -subj {info} -out {csr_path}')
    system(f'openssl x509 -req -sha256 -in {csr_path} -CA {ca_cert_path} -CAkey {ca_key_path} -CAcreateserial -days {time} -extfile v3.ext -out {cert_path}')


def generate_private_key(filename: str = 'default.key', leng: int = 2048): # 生成新私钥
    system(f'openssl genrsa -out {filename} {leng}')
    return


def init_path(): # 模块：初始化目录
    system('touch index.txt serial')
    system('echo 1 >> serial')
    system('mkdir ca')
    return


def make_config():
    f = open("v3.ext",'w')
    f.write('subjectAltName = @alt_names\n\n[alt_names]\n')
    count: int = 1
    while True:
        dns_name: str = input(f'请输入您SSL证书的域名{count}(支持通配)(输入0以结束): ')
        if dns_name == '0':
            break
        if dns_name != '0':
            f.write(f'DNS.{count} = {dns_name}\n')
            count = count+1
    f.close()
    return


if __name__ == '__main__':
    main()
