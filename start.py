# -*- coding:UTF-8 -*-
import main
import time

while True:
    try:
        main.main()
    except Exception as e:
        print(e)
        time.sleep(3)
        continue
