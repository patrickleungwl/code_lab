using System;

namespace CSharpExercises
{
    public class DummyClassUsingCSharpVersion1
    {
        private string _name;
        public string Name
        {
            get
            {
                return _name;
            }
        }

        public DummyClassUsingCSharpVersion1(string name)
        {
            _name = name;
        }
    }
}
