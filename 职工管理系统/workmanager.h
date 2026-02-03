#pragma once
#include<iostream>
#include<fstream>
#include<vector>
#include<memory>
#include<string>
#include<algorithm>

class worker
{
public:
	int m_id;
	std::string m_name;
	int m_dep;//1.employee 2.manager 2.boss
	virtual void show_info() = 0;
	virtual std::string get_dep() = 0;
	worker(int id, std::string name, int dep) :m_id(id), m_name(name), m_dep(dep){}
	virtual ~worker() {};
};

class employee :public worker
{
public:
	employee(int id, std::string name, int dep):worker(id,name,dep){}
	void show_info()
	{
		std::cout << m_id << " " << m_name << " " << get_dep() << std::endl;
	}

	std::string get_dep()
	{
		return "employee";
	}

};

class manager :public worker
{
public:
	manager(int id, std::string name, int dep) :worker(id, name, dep) {}
	void show_info()
	{
		std::cout << m_id << " " << m_name << " " << get_dep() << std::endl;
	}

	std::string get_dep()
	{
		return "manager";
	}

};

class boss :public worker
{
public:
	boss(int id, std::string name, int dep) :worker(id, name, dep) {}
	void show_info()
	{
		std::cout << m_id << " " << m_name << " " << get_dep() << std::endl;
	}

	std::string get_dep()
	{
		return "boss";
	}

};

class worker_manager
{
public:
	worker_manager();
	void add_worker();
	void delete_worker();
	void show_worker();
	void save_to_file();
	void load_from_file();
	void is_exist();
	void sort_file();
	void clear_file();
private:
	std::vector<std::unique_ptr<worker>>pv;
};

bool compare1(const std::unique_ptr<worker>& A, const std::unique_ptr<worker>& B);
bool compare2(const std::unique_ptr<worker>& A, const std::unique_ptr<worker>& B);
