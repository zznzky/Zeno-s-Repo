#include"workmanager.h"

worker_manager::worker_manager()
{
	this->load_from_file();
}

void worker_manager:: save_to_file()
{
	std::ofstream ofs("职工管理系统.txt", std::ios::out | std::ios::trunc);
	for (auto& p : pv)ofs << p->m_id << " " << p->m_name << " " << p->m_dep<< std::endl;
	ofs.close();
}

 void worker_manager::load_from_file()
{
	 std::ifstream ifs("职工管理系统.txt", std::ios::in);
	 if (!ifs.is_open())return;
	 int id;
	 std::string name;
	 int dep;
	 while (ifs >> id >> name >> dep)
	 {
		 if (dep == 1)pv.push_back(std::make_unique<employee>(id, name, dep));
		 else if (dep == 2)pv.push_back(std::make_unique<manager>(id, name, dep));
		 else pv.push_back(std::make_unique<boss>(id, name, dep));
	 }
	 ifs.close();
}

 void worker_manager::add_worker()
 {
	 int id;
	 std::cout << "请录入编号\n";
	 while (!(std::cin >> id))
	 {
		 std::cout << "请输入数字\n";
		 std::cin.clear();
		 std::cin.ignore(1000, '\n');
		 return;
	 }
	 for (auto& p : pv)
	 {
		 if (id == p->m_id)
		 {
			 std::cout << "当前编号已存在\n";
			 return;
		 }
	 }
	 std::cin.ignore(1000,'\n');
	 std::string name;
	 std::cout << "请录入姓名\n";
	 std::getline(std::cin, name);
	 std::cout << "\n请录入岗位: 1.employee 2.manager 3.boss\n";
	 int dep;
	 while (true) {
		 std::cin >> dep;
		 if (dep == 1)
		 {
			 pv.push_back(std::make_unique<employee>(id, name, dep));
			 this->save_to_file();
			 std::cout << "添加成功\n";
			 return;
		 }
		 else if (dep == 2)
		 {
			 pv.push_back(std::make_unique<manager>(id, name, dep));
			 this->save_to_file();
			 std::cout << "添加成功\n";
			 return;
		 }
		 else if (dep == 3)
		 {
			 pv.push_back(std::make_unique<boss>(id, name, dep));
			 this->save_to_file();
			 std::cout << "添加成功\n";
			 return;
		 }
		 else
		 {
			 std::cout << "请输入正确的数字\n";
			 std::cin.clear();
			 std::cin.ignore(1000,'\n');
		 }
	 }
 }

 void worker_manager::delete_worker()
 {
	 std::cout << "请输入删除对象的编号\n";
	 int id;
	 std::cin >> id;
	 for (auto it = pv.begin();it != pv.end();it++)
	 {
		 if ((*it)->m_id == id)
		 {
			 pv.erase(it);
			 std::cout << "删除成功\n";
			 this->save_to_file();
			 return;
		 }
	 }
	 std::cout << "删除对象不存在\n";
	 return;
 }

 void worker_manager::show_worker()
 {
	 if (pv.empty())
	 {
		 std::cout << "当前暂无员工\n";
		 return;
	 }
	 for (auto& p : pv)
	 {
		 std::cout << p->m_id << " " << p->m_name << " " << p->get_dep() << std::endl;
	 }
 }

 void  worker_manager::is_exist()
 {
	 int id;
	 std::cout << "请输入编号\n";
	 std::cin >> id;
	 for (auto& p : pv)
	 {
		 if (id == p->m_id)
		 {
			 std::cout << "查找成功\n";
			 p->show_info();
			 return;
		 }
	 }
	 std::cout << "查无此人\n";
 }

 void  worker_manager::sort_file()
 {
	 if (pv.empty())return;
	 int i = 0;
	 std::cout << "请输入排序方式(1.升序 2.降序)\n";
	 std::cin >> i;
	 if (i == 1)
	 {
		 std::sort(pv.begin(), pv.end(), compare1);
		 std::cout << "排序成功\n";
		 this->save_to_file();
	 }
	 else if (i == 2)
	 {
		 std::sort(pv.begin(), pv.end(), compare2);
		 std::cout << "排序成功\n";
		 this->save_to_file();
	 }
	 else return;
 }

 void  worker_manager::clear_file()
 {
	 std::cout << "请再次确认 (1.清空 2.返回)";
	 int i;
	 std::cin >> i;
	 if (i == 1)
	 {
		 std::ofstream ofs("职工管理系统.txt", std::ios::out | std::ios::trunc);
		 ofs.close();
		 pv.clear();
		 std::cout << "文件清空成功\n";
		 return;
	 }
	 else return;
 }

 bool compare1(const std::unique_ptr<worker>& A, const std::unique_ptr<worker>& B)
 {
	 return A->m_id < B->m_id;
 }

 bool compare2(const std::unique_ptr<worker>& A, const std::unique_ptr<worker>& B)
 {
	 return A->m_id > B->m_id;
 }
