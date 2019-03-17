using System;

namespace CSharpExercises
{
    public class DummyClassUsingCSharpVersion2
    {
        private string _name;
        public string Name
        {
            get
            {
                return _name;
            }
            private set
            {
                _name = value;
            }
        }

        public DummyClassUsingCSharpVersion2(string name)
        {
            _name = name;
        }
    }
}
