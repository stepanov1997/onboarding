import sys

from metaflow import step, FlowSpec, retry, catch, timeout


class TestMetaflow(FlowSpec):

    @step
    def start(self):
        self.next(self.a, self.b, self.c)

    @step
    def a(self):
        self.variable1 = 1
        self.next(self.join)

    @step
    def b(self):
        self.variable2 = 3
        self.next(self.join)

    @step
    def c(self):
        self.variable3 = 9
        self.next(self.join)

    @step
    def join(self, inputs):
        self.merge_artifacts(inputs)
        print(self.variable1)
        print(self.variable2)
        print(self.variable3)
        self.next(self.one)

    @step
    def one(self):
        self.collection = [self.variable1, self.variable2, self.variable3]
        print(self.collection)
        self.next(self.for_consumer, foreach='collection')

    @step
    def for_consumer(self):

        print(self.collection)
        self.variable = self.input
        setattr(self, f"var{self.collection.index(self.variable)}", self.variable*2)
        self.next(self.join_2)

    @retry(times=1)
    @catch(print_exception=False, var='exception')
    @timeout(seconds=3)
    @step
    def join_2(self, inputs):
        self.merge_artifacts(inputs, exclude=['variable'])
        print("var0=", self.var0)
        print("var1=", self.var1)
        print("var2=", self.var2)
        self.next(self.end)

    @step
    def end(self):
        if self.exception:
            print(self.exception)
            sys.exit(1)


if __name__ == "__main__":
    TestMetaflow()
