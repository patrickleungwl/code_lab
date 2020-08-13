#include <iostream>
#include <map>
#include <vector>

using namespace std;


class TestClass
{
public:
    explicit TestClass(double d) : _d(d) {};
private:
    double _d;
};


void testExplicitKeyword()
{
    vector<TestClass> v1;

    // with explicit keyword in constructor
    // this is no longer legal
    // v1.push_back(1.0);

    // have to say this
    v1.push_back(TestClass(1.0));
}


void testMultiMap()
{
    multimap<string, int> mm{
        {"mickey", 100},
        {"minnie", 150},
        {"mickey", 200},
        {"minnie", 300},
        {"minnie", 400}
    };

    cout << "mickey count " << mm.count("mickey") << endl;
    cout << "minnie count " << mm.count("minnie") << endl;
    auto res = mm.equal_range("mickey");
    for (auto iter=res.first; iter != res.second; ++iter) {
        cout << iter->first << " " << iter->second << endl;
    }
    res = mm.equal_range("minnie");
    for (auto iter=res.first; iter != res.second; ++iter) {
        cout << iter->first << " " << iter->second << endl;
    }
    // erase just the second instance of minnie
    // reverse iterate because erasing a member removes 
    // member from container
    for (auto iter=res.second; iter != res.first; --iter) {
        if (iter->second>=300) {
            iter = mm.erase(iter);
        }
    }
    cout << "after erasing select instances of minnie" << endl;
    res = mm.equal_range("minnie");
    for (auto iter=res.first; iter != res.second; ++iter) {
        cout << iter->first << " " << iter->second << endl;
    }
}


void testInitialisingVectors()
{
    // initialise the old way
    vector<int> v1;
    v1.push_back(1);
    v1.push_back(2);

    // initialise the new way
    vector<int> v2{1,2};

    // initialise using with and without =
    vector<int> v3 = {1,2};


}


void testInitialisingMaps()
{
    // initialise the old way
    map<int, string> m1;
    m1[1] = "hello";
    cout << "m1 " << 1 << "->" << m1[1] << endl;
    
    // another old way
    typedef map<int, string>::iterator miter;
    pair<miter, bool> result = m1.insert( pair<int, string>(2,"world") );
    if (result.second) { 
        cout << "m1 " 
             << (result.first)->first 
             << "->" << (result.first)->second << endl;
    } else {
        cout << "m1 failed to insert" << endl;
    }

    // reinsert same key again
    pair<miter, bool> result2 = m1.insert( pair<int, string>(2,"world") );
    if (result2.second) { 
        cout << "m1 " 
             << (result2.first)->first 
             << "->" << (result2.first)->second << endl;
    } else {
        cout << "m1 failed to insert great!" << endl;
    }

    // initialise the new way
    map<int,string> m2{
        {1, "hello"},
        {2, "world"}
    };

    cout << "m2 " << 1 << "->" << m2[1] << endl;
    cout << "m2 " << 2 << "->" << m2[2] << endl;

    // initialise the new way with =
    map<int,string> m3 = {
        {1, "hello"},
        {2, "world"}
    };
}


int main() 
{
    testExplicitKeyword();
    testMultiMap();
    testInitialisingVectors();
    testInitialisingMaps();
}


