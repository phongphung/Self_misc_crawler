from flask import Flask
import wmi

app = Flask(__name__)

ip = ['server1', 'server2', 'server3', 'server4', 'server5']
user = "username"
password = "password"
append_services = []

words = 'win32'


@app.route("/")
def service_status():
    results = []  # Temp for result to return to html
    for a in ip:
        global append_services
        print('\n'+a+'\n')
        c = wmi.WMI(a, user=user, password=password)
        get_names = c.Win32_Service()

        for y in get_names:
            convert = str(y.Name)
            append_services.append(convert)
            append_services = \
                [w for w in append_services if w.startswith(words)]

        for l in append_services:
            state_of_services = c.Win32_Service(Name=l)
            if state_of_services:
                for x in state_of_services:
                    convert1 = str(x.State)
                    convert2 = str(x.Caption)
                    results.append([a, [convert1, convert2]])  # Append results
                    print(convert1 + "        " + convert2)

    # This part for generate HTML for return
    html = ''
    for i in results:
        html += '<h2>Ip: ' + i[0] + '</br>'
        html += '<h3>From ' + i[0][0] + ' to ' + i[0][1]

    return html

if __name__ == "__main__":
    app.run()
