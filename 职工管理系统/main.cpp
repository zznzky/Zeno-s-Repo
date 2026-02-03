#include"workmanager.h"

void menu()
{
	std::cout << "欢迎进入职工管理系统\n";
	std::cout << "*** 1.录入 ***\n";
	std::cout << "*** 2.查询 ***\n";
	std::cout << "*** 3.删除 ***\n";
	std::cout << "*** 4.全览 ***\n";
	std::cout << "*** 5.排序 ***\n";
	std::cout << "*** 6.清空 ***\n";
	std::cout << "*** 0.退出 ***\n";
}

int main()
{
	worker_manager worker;
	int i = 0;
	while (true)
	{
		menu();
		std::cin >> i;
		switch (i)
		{
		case 1:worker.add_worker();break;
		case 2:worker.is_exist();break;
		case 3:worker.delete_worker();break;
		case 4:worker.show_worker();break;
		case 5:worker.sort_file();break;
		case 6:worker.clear_file();break;
		case 0:std::cout << "欢迎下次使用";return 0;
		default:break;
		}
	}
}
