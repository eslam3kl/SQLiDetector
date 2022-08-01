# SQLiDetector
Simple python script that helps you to detect SQL injection "Error based" by sending multiple requests with 9 payloads and checking for 152 regex patterns for different databases.

![Header](https://github.com/eslam3kl/SQLiDetector/blob/main/SCREENSHOT.png)

## Description
The main idea for the tool is scanning for Error Based SQL Injection by using different payloads like
```
' 
"
'' Double Singel quote
"" Double Double quote
'" Single quote + Double qoute
"' Double quote + single quote
") 
')
\
[]
```
And match for 152 error regex patterns for different databases. <br />
Source: https://github.com/sqlmapproject/sqlmap/blob/master/data/xml/errors.xml

## How does it work? 
It's very simple, just organize your steps as follows
1. Use your subdomain grabber script or tools. 
2. Use your links and URLs tools to grab all waybackurls. 
3. Use URO tool to filter them and reduce the noise. 
4. Grep to get all the links that contain parameters only. You can use Grep or GF tool.
5. Pass the final URLs file to the tool, and it will test them. 
```
pip3 install -r requirements.txt [Just for the first time only]
python3 sqli_detector.py <waybackurls_file.txt>
```

## How does it test the parameter? 
What's the difference between this tool and any other one? 
If we have a link like this one, `https://example.com?file=aykalam&username=eslam3kl` so we have 2 parameters. It creates 2 possible vulnerable URLs. 
1. It will work for every payload like the following 
```
https://example.com?file=123'&username=eslam3kl
https://example.com?file=aykalam&username=123'
```
2. It will send a request for every link and check if one of the patterns is existing using regex. 
3. For any vulnerable link, it will save it at a separate file for every process. 

## Upcoming updates
- [ ] Adding threads to increase the speed.
- [ ] Adding more payloads.
- [ ] Enhance the output schema.
- [ ] Adding progress bar.

If you want to contribute, feel free to do that. You're welcome :)

## Contributors
Thanks to Mohamed El-Khayat and Orwa for the amazing paylaods and ideas. Follow them and you will learn more
```
https://twitter.com/Mohamed87Khayat
https://twitter.com/GodfatherOrwa
```

## Stay in touch <3 
[LinkedIn](https://www.linkedin.com/in/eslam3kl/) | [Blog](https://eslam3kl.medium.com/) | [Twitter](https://twitter.com/eslam3kll)
