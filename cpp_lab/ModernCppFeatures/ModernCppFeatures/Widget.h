#pragma once


class Widget
{
public:
	Widget(int i);
	~Widget();

	//Widget(Widget& other);
	Widget(const Widget &other);
	Widget &operator=(const Widget &other);

	Widget(Widget &&other) noexcept;
	Widget &operator=(Widget &&other) noexcept;

	// used by find
	bool operator==(const Widget &other) const;

	// used for sorting by set container
	bool operator<(const Widget &other) const;

	int getId() const;
	int getContents(int memId) const;
	void updateId(int i) { _id = i;  }

	static int widgetCount;
	static int assignmentCount;
	static int copyConstructorCount;
	static int moveConstructorCount;

private:
	int _id;
	int *pmemory;

	const int widget_size = 100000;
};



class Comparators
{
public:
	bool operator() (const Widget &left, const Widget &right)
	{
		return left.getId() > right.getId();
	}
};
