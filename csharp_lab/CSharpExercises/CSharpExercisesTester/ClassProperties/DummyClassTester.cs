using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using CSharpExercises;

namespace CSharpExercisesTester
{
    [TestClass]
    public class DummyClassTester
    {
        [TestMethod]
        public void TestDummyClassUsingCSharpVersion1()
        {
            var item = new DummyClassUsingCSharpVersion1("Jane");
            Assert.AreEqual("Jane", item.Name);
        }

        [TestMethod]
        public void TestDummyClassUsingCSharpVersion2()
        {
            var item = new DummyClassUsingCSharpVersion2("Jane");
            Assert.AreEqual("Jane", item.Name);
        }

        [TestMethod]
        public void TestDummyClassUsingCSharpVersion3()
        {
            var item = new DummyClassUsingCSharpVersion3("Jane");
            Assert.AreEqual("Jane", item.Name);
        }
    }
}
