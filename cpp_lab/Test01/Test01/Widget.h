#pragma once


class Widget
{
public:
	Widget(int i);
	~Widget();

	Widget(const Widget &other);
	Widget &operator=(const Widget &other);

	Widget(Widget &&other);
	Widget &operator=(Widget &&other);

	bool operator==(const Widget &other) const;
	bool operator<(const Widget &other) const;

	int getId() const;
	int getContents(int memId) const;

private:
	int _id;
	int *pmemory;

	const int widget_size = 100000;
};