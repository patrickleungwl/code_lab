#include <iostream>
#include <map>
#include <vector>


using namespace std;

struct price {
private:
    int _item_id;
    double _ask_price;
public:
    price(int item_id, double ask_price) :
        _item_id(item_id),
        _ask_price(ask_price) {
        cout << "ctr" << endl;
    }

    price(const price& rp) {
        cout << "copyctr" << endl;
        _item_id = rp._item_id;
        _ask_price = rp._ask_price;
    }

    virtual ~price() {
        cout << "dtr" << endl;
    }

    price(price &&p) {
        cout << "movectr" << endl;
        _item_id = p._item_id;
        _ask_price = p._ask_price;
    }

    price& operator=(price &&p) {
        if (this != &p) {
            _item_id = p._item_id;
            _ask_price = p._ask_price;
        }
        return *this;
    }
    
    inline int get_item() const { return _item_id; }
    inline double get_price() const { return _ask_price; }
};

ostream& operator<<(ostream &s, const price& p) {
    s << p.get_item() << ", " << p.get_price();
}


auto get_list_of_prices(int shop_id) {

    vector<price> shop_prices;
    for (int i=0; i<1; i++) {
        shop_prices.push_back(price(shop_id+i,shop_id*i));
    }

    return shop_prices;
}


int main() {

//   cout << "hello" << endl;
//   price p(100,99.9);
//   cout << p << endl;

    cout << "*** creating a map to vector" << endl;
    map<int, vector<price>> shop_prices;

    cout << "*** creating first shop of prices" << endl;
    shop_prices[0] = get_list_of_prices(0);
    cout << "*** creating second shop of prices" << endl;
    shop_prices[1] = get_list_of_prices(1);

    for (int shop=0; shop<2; shop++) {
        cout << "***  reading shop " << shop << endl;
        auto prices = shop_prices[shop];
        int i=0;
        cout << "item/price=";
        for (auto p : prices) {
            cout << "(" << p << "), ";
        }
        cout << endl;
    }
}


