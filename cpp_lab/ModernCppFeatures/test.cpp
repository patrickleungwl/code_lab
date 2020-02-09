#include <iostream>
#include <map>
#include <vector>


using namespace std;

struct bigObject {
private:
    int _item_id;
    vector<double> *_prices;
public:
    bigObject(int item_id) :
        _item_id(item_id) {
        cout << "ctr" << endl;
        _prices = new vector<double>(100);
    }

    bigObject(const bigObject& rp) {
        cout << "copyctr" << endl;
        _item_id = rp._item_id;
        _bigObjects = new vector<double>(100);
        for (int i=0; i<100; i++ ) {
            _prices[i] = rp._prices[i];
        }
    }

    virtual ~bigObject() {
        cout << "dtr" << endl;
    }

    // move constructor makes a fast copy of internal data
    // the original data pointer must be set to null
    bigObject(bigObject &&rp) {
        cout << "movectr" << endl;
        _item_id = rp._item_id;
        _bigObjects = rp._bigObjects;
        rp._bigObjects = nullptr;
    }

    bigObject& operator=(bigObject &&p) {
        if (this != &p) {
            _item_id = p._item_id;
            _ask_bigObject = p._ask_bigObject;
        }
        return *this;
    }
    
    inline int get_item() const { return _item_id; }
    inline double get_bigObject() const { return _ask_bigObject; }
};

ostream& operator<<(ostream &s, const bigObject& p) {
    s << p.get_item() << ", " << p.get_bigObject();
}


auto get_list_of_prices(int shop_id, int num_items) {

    vector<price> shop_prices;
    for (int i=0; i<num_items; i++) {
        shop_prices.push_back(price(shop_id+i,shop_id*i));
    }

    return shop_prices;
}


int main() {

    cout << "*** creating list of prices" << endl;
    vector<price> prices = get_list_of_prices(0,1);

    cout << "iteration start" << endl;
    for (auto p : prices) {
        cout << "(" << p << "), " << endl;
    }
    cout << "iteration end" << endl;
}


