## 文件分割成小文件
	
运行

	python split.py --file arg1 --line arg2 --name arg3  --dir arg4

		--file  将要分割的文件
		--line  每个文件的行数
		--name  新文件的名字
		--dir   新文件存放的路劲

##
实例
    
    python split.py --file a.txt --line 60 --name new  --dir newdir

如果文件a.txt 有350行，将会生成6个文件，前5个文件有60行第6个文件有50行，文件夹newdir 将生成文件 new.0 new.1 new.2 new.3 new.4 new.5








