Hunter Mast
PA4 readme.txt

	When starting on the type checker, I first started with the PA4Starter.py file given to us and watched Dr. Leach's video on how to start type checking. There is not a ton when starting with this. I mostly had a few class formats and some basic type checking when it came to some simple statements like 'Plus'. Eventually, I would expand it to be the type checker I have currently. It still has some issues I plan to iron out before fully turning it in, but I wanted to go over the basics of how it was created, formatted, and what I implemented for type checking.

Format:
	When starting to create the type checker, I started with trying to create a format following what was given to us. This means that I started by reading in the input file with whitespace included, then creating an ast with it. We go through a function called read_ast() that will start to format our parsed input into a readable format for our type checker. Inside of it, I hardcoded in all of our different internal classes. I wanted to make it so I could directly input all of the methods by calling the specific class needed to create them. Most of them have only methods they use and all inherit from the "Object" class, so I had to implement that feature also. From our parsed AST file, we read the number of classes at the beginning and start to loop through the amount given to us. We call read_class() and then start reading class information. We find our if it has any inheritance and then register it's parent class as "Object" if it inherits nothing, or get it's specific inheritance. We then will find the number of features the class has to we can loop through that. We then add the number of features to a feature_list by calling read_feature(). read_feature() reads the feature kind listed and will start to gather information on it's specified type between attribute with no initialization, attribute initialized, and methods. We also, specifically with methods, run read_formal() and get the arguments each method has. Inside of sorting these, we also run read_exp(). read_exp() is a large function that will read in the line number, expression name, and then depending on the expression, gather information from the parsed AST file that relates to the expression. This section is not too thrilling. It mostly is just following the format PA3 outputs and gathers all of that information. We then are calling lots of different classes here that will format the information gathered on each expression, feature, and class into a layered and readable format for our type checker to see how the file was actually being formatted and storing information on each expression, feature, and class. I chose the way these classes were formatted not for any specific reason. This was how the starter file was given to us, so I decided to mostly copy and paste that format and apply it to all of our different classes. Something that was included in the starter file I did not deal with too much were keeping track of tabs. It seemed like for the most part they did not affect readability from my type checker, so I mostly left the format for them all the same throughout my expressions. Optimally, I would remove these and clean up how the classes are formatting with tabs, but it's not important to the rest of my code except readability for debugging.

Type Checking:
	This is the large part of this assignment. With this AST created, we check if the classes themselves have any sort of inheritance cycle. Checking for inheritance is done by doing a depth first search, similarly to our first assignment in this class. We keep track of each class we visit and then continue to check for inheritance to make sure none of our classes overlap. If our AST file does not have any inheritance cycles, we continue on. We then start to do some basic type checking with classes, methods, and attributes before we go more indepth with their features. We start with checking class names themselves. We try and make sure they are not defined multiple times. Each class we find is added to a list of named classes. This is done first just because I also am checking for cycles first, which is similar. We then check for the Main class. It must exist so if we do not find it, we throw an error. If we do though, we then search to see if it has any instance of a method called 'main'. This must exist in the Main class, so we throw an error if it does not exist. Next, we continue through to start checking class inheritance. We need to make sure that what we are inheriting is another class that exists. We use that named class list to see if our inherited identifier exists. If not, we throw an error. If it is Int, String, or Bool, we also throw an error as we cannot inherit from these. The next section involves some basics for attributes and methods, without dealing with feature bodies. This is because those involve expressions and can become a lot more complicated very fast. In this section, we go through each feature of each class and if the attribute or method does not have a return type that is the name of a class (Including internal names) or of the types Int, String, Bool, or SELF_TYPE, we throw an error. With methods, it becomes a bit more complex as we need to check formals. Formals cannot be redefined, so we check each parent class that we inherit's methods to make sure each formal is different. We also ake sure that the amount of parameters match. There is one exception to this we need to check and that is the main method. If we come accrossed the main method, it should never have any formals. We need to check that and throw an error if anything else occurs. 
	After all of that basic type checking, we start to get ready for dealing with feature bodies and expressions. We first set up our symbol table. This was provided in our starter file, but I had some issues with it. I could not figure out how to make it remember between classes which attributes exist and which methods are inherited, so I decided to make it a global variable. We keep track of what we are inheriting from, attribute names, and method names. This will be very useful when checking for inherited features. We also formalize the internal classes into the symbol table for when needing to look at it's methods. This, to me, was more useful at keeping track of the overall structure of our program compared to our classes at the beginning of the code, which just keep track of certain instances.
	After setting up our symbol table, we then start to go through our type checker. Since we added the internal classes to our symbol table manually, we do not send those through as they do not need type checked. We start with going through classes again to format the symbol table. When getting an instance of class, because of our class structure, attributes and methods would also recognized by instances of classes. To solve this, we just add that we are only looking for classes in this section. We check and make sure the symbol table has all of it's sections filled out like inheritance, attributes, and methods. We also recursively call typeCheck() on each attribute and method. Doing this, we can not only verify how attribtue and method types are, but also start to look at the expressions in each feature body. The only error we have in this section is that if the attribute initialization type is not the same as the attribute type itself, we throw an error.
	In our attribute section, we start by making sure that the attribute name is not self, as this will throw an error. We also go through each parent class and attribute to mae sure we are not overriding any. If not, we add the new attribute type to our table and check initialization. If that also passes again, we return the feature type.
	In our method section, we get a bit more complicated than our attributes. We first try to make sure wee do not have any parameters that are 'SELF_TYPE'. After this, we then start to go through each parent class we inherit and check every method. If we redefine any parameters, we throw an error. This can become a bit complicated as there is a lot of looping here, but we just keep track of the parent class until it reachs Object, which has no inheritance. After that, we cehck if we define our method name as any that are internally defined. The easiest way for me to do this is just to create a small list with all of the names that cannot be used inside of it. There are probably more efficeint ways, but this seemed to work the best. We also check that the method has a class. There are not very many circumstances that one would not, but it doesn't hurt to check. We then go through each formal to make sure thre are no duplicates. This is done by just keeping a set as we loop through them and if any already exist in the set, we throw an error. We also check here that if the method name is self or SELF_TYPE, we throw an error. After all of that is done, we then call typeCheck() on our feature body to start with the expressions inside and return the method's type.
	In the Assign section, we are dealing with trying to assign identifiers to values. We start off by making sure we are not assigning anything to self as it's just not possible. If we already have the value in our symbol table, we get that type. If not, we search for it throughout inheritance. If we cannot find it, we throw an error. We then get the type for t2. If they are not the same, we then check if they conform. This is because sometimes the types will work, even if they are not equal. If they do not conform, we throw an error.
	In dynamic dispatch, static dispatch, and self dispatch are all pretty similar. With dynamic dispatch, we first check the object (Class) and make sure that it exists. If so, we then get information on the method we are dispatching from. If that method does not exist, then we also throw an error. After this, we check the number of arguments in the method to make sure they match. Any mismatch will throw an error. There was a section in each of these instances that would search for bad arguments if the formal type did not match the argument type, but it was causing too many errors I just removed this part. We would then just return the correct class type we dispatched from. All of these are the same except static and self are a bit different. With static, I had to make sure that the object type conformed with the static class type. If not, we would throw an error. For self dispatch, there is no object type. Instead, since it's self dispatch, the type is just the current class. Overall, this section was very complicated and cause me lots of issues. Yet, I got the rest to work for the most part, even though this part isn't as well done as the rest. baddispatch.cl and badargs1.cl, badargs2.cl, and badargs3.cl all seem to not encounter any errors.
	In the If section,  we check the predicate first to make sure it is a Bool type. If not, we throw and error. The rest of this section is checking the then statement and if there is an else section, getting it's type. Once we have those, we compare them and get the resulting type.
	In the While section, we pretty much do the same thing as the If section. We make sure the predicate is Bool. If not, throw an error. We also here need to make sure that the body is not SELF_TYPE. Otehrwise, we throw an error. The While statement is always the type Object, so we assign that and move to the next section.
	In the Block section, we are just looping through every expression inside of it. The block itself should be the type of the last expression, so we should just assign it to that type. Fairly simple.
	In the New and IsVoid sections, we are doing pretty much the same thing. For New, we get the expression and that is the type. For IsVoid, we typecheck the expression, but it is always Bool. This is because the expression must be typechecked, but has to send back Bool.
	In the Plus, Minus, Multiply, and Divide sections, we are just checking that both expressions we are looking at are of the type Int. Otherwise, we just throw an error. Very easy implementation.
	In the Lt and Le, we are doing something similar to the Plus, Minus, etc. sections. We check that both types are Int and if not, we throw an error. The big difference is that these return Bool instead of Int.
	In the Eq section, we check that both of our expressions are Int, Bool, or String. If they are one of these, we then compare those. If they are not the same, we throw an error. Otherwise, if neither of them are Int, Bool, or String, we should allow them to be compared. We also check that if there are void cases that match each other. If not, we throw an error. This should return a Bool type always.
	In the Not and Negate sections, we are checking an expression to make sure it is a specific type. We throw an error if not. For Not, we must have type Bool. This is for if-statements and others like that. For Negate, we need Int. This is for negative numbers and such. Both will return their respective types.
	In the Let section, we go through the let binding to see scoped assignment and find the body's type. Since this has variables only available in this scope, we copy the symbol table to a temporary variable that once we finish this expression for let, we revert it back.  This idea is also used in the Case section. WIn our class, I made my binding into a tuple with the identifier, type, and value (If there is one). If the identifier is named 'self', then we throw an error. If the value exists, we then type check it. If it does not match the identifier we are initializing, we throw an error. We also handle object assignment. We then will continue to add to the symbol table the identifier and type throughout. Once we finish with this, we then run the body. Since we have been updating our original symbol table, we can access all of these let variables. After we finish with the body, we revert the symbol table back and return the body's type.
	In the Case section, we do something very similar to let. The big different is that we get the result type from if all types are the same. Otherwise, case has the type of Object. While unpacking our expression, we have 2 errors. One is that we must have different types for each expression. For it, we just keep track of types we've seen. We also cannot use SELF_TYPE. Overall, it's just the Let section, but slightly changed on how the return type is found.
	In the Identifier section, we go through and need to complete a variety of checks. First, we assign self and SELF_TYPE right away as I've had issues with getting those assigned correctly before. Later on in my program when serializing expressions, I explicitly reassign self as for some reason, it does not like to assign itself. Weird bug, but this fix seems to work. We then check if our value is in our symbol table. If not, we then start going through all of our attributes and methods to check if we have it anywhere in our symbol table. If it is out of scope or not found, we throw an error.
	In the Integer, String, and Bool sections, we are just checking returning the type. This is more for the rest of the type checker to know what we are comparing or looking at.
	If none of these are found, we return an error as we should never be getting None as a type.


File Writing:
	After all of our type checking, we finish by writing this all to a file. Since this was to be made alphabetically, for all of our maps (Class map, implementation map, and parent map), we start by creating sorted_classes using Python's built-in sorted() function. With that done, we start to write in the order desired. Two sections I wanted to mention are the collect_parent_methods() and collect_parent_attributes() functions. These collect all of the names of methods and attributes from inheritance, including internal classes. This is done here just for the simplicity of writing and not needing to look back to symbol table. I could have included them in the section where we write to the file, but it reads better if we have it separated. I originally had recursion with it too, but I removed it and didn't realize I could move it back down to where we write. Once we need to start writing expressions, we do all of that from our serialize_expression() function. We call serialize_internal() for all of the internal classes since those are formatted a bit differently. serialize_expression() is called multiple times, so is it's own function to save on space. It just writes depending on the expression from whatever feature body is given. Other than that, a lot of this is just going through each class alphabetically and writing depending on the requirements, so nothing too special. Something I had to add that was a bit tricky was while writing the annotated AST, I forgot about checking Object itself being inherited. I had changed the original starter code from starting with None to starting with Object being inherited. This led to the end when classes should inherit nothing inherit Object. When inheriting from Object and directly calling that, it does need to say it inherits from Object. I would change it back to None inheritance, but then none of the internal methods were being recognized when called on. I used arith.cl mostly as my testing file, so this helped me look at inheritance since there is a lot in that file. I ended up changing it to None and when it finished reading the AST, we change it all back to Object and added which already were inheriting to a check. Adding a check inside of each class that if we are directly inheriting from Object fix this issue. This is just one example of a feature that needed to be added for my output and the complexities this brought me.

good.cl:
	This test case actually ran. bad3.cl plays off of it and tries to make a bad version of this. good.cl though does very well in having a variety of different aspects to deal with. There are let sstatements for out of scope checking, There are different attributes that are inherited, classes are inherited from one another, there are assignments, if-statements for looking at predicates, while-statements for the same, etc. There are a lot of aspects that really work well for checking types in this class and I think it is a great example.

bad1.cl:
	Test case bad1.cl has a focus on dispatch. Currently, it has a few issues implemented inside of it. One bit one is that it is handling 2 different Main classes and 2 different B classes. On top of this, there is a non-existant method on line 15 that will always run into an error. One of the Main classes doesn't inherit IO when it should. There are quite a bit of different issues I implemnted dealing with classes and method calls. While I struggled with getting dispatch to work, I believe this will throw an error, at least at first about there being 2 Main classes.

bad2.cl:
	This one has a focus in the case method and shows some other issues involving classes. One is that class A and class B have an inheritance cycle. Following this, the case expression has multiple Int types inside that should not exist. The Main class has 2 large issues. One is that the main method is taking in parameters when it should not have any. The second is Main inherits Int, which should not be the case. In class A, in the let-statement, there is a case-statement that has multiple of the same type. With that, there is also the variable, x, which should be out of scope. This also shows a lot of different situations that I handle in my class involving a wide array of topics.

bad3.cl:
	In bad3.cl, I added a few different conditions that do not work exactly how they should. This is actually the same code as good.cl, but it has some issues added to it. One is that self is being assigned to. The case expression also does not work and is being assigned multiple fo the same variable. Line 108 has an issue where the then-statement is just a number. The predicate for the if-statement is comparing Int to Bool, which is not allowed. In calculate(), result is of type A, which Int should not conform to. Overall, it has a lot of different issues added in that I feel encapsulate a lot more of the errors regarding types themselves, rather than the other two bad test cases.

Conclusion:
	Overall, I feel like I learned a lot from this project. It was fun to try and figure out how to connect each identifier and keep track of types. Debugging was very hard though as I started by writing it all, then went back and was trying to debug class_map only. There are a lot of way to optimize this. I believe there are multiple checks for the same error, which isn't necessarily needed and takes up a lot of space. A lot of functions could be separated too to not use as many lines. Readability is also something I wish I focused on more. It makes sense after you look for awhile, but not using a good variable name and instead calling each class and it's variables just gets really long and confusing. The section I struggled on the most was dispatch. For some reason, when I added argument errors, it would mess with a lot of existing test cases. Trying to get them all to work together also and determine which type of dispatch was tough. SELF_TYPE also gave me issues as I never knew when to pass it. It got easier as it went on and I was able to figure most of it out, but there were still a few that didn't work correctly. The most interesting part to me with the assignment was how class hierarchy was created. It was cool to see it go from AST file to being formatted in a way similar to normal source code. It was a bit hard to figure out how to deal with what features of each class, but eventually I learned how the hierarchy was and it wasn't too bad. I feel very happy with my finished type checker and might work sometime in the future to improve any errors I was experiencing.

List of Type Checking Rules:
Attribute type mismatch
Atrtribute cannot be named 'self'
Attribute cannot be overridden from inherited class
Method should not be type 'SELF_TYPE'
Class redefines method
Internal method cannot be overridden
No class information for method
Method has duplicate formals
Method formal cannot be 'self'
Method formal cannot be 'SELF_TYPE'
Cannot assign 'self'
Variable has not been declared
Identifier cannot be assigned to itself
Assign expressions do not conform
Class not found for dynamic dispatch
Method not found for dynamic dispatch
Method arguments mismatched for dynamic dispatch
Type does not conform for static dispatch
Method not found for static dispatch
Method arguments mismatched for static dispatch
Method not found for self dispatch
Method arguments mismatched for self dispatch
If-statement predicate should be type 'Bool'
While-statement predicate should be type 'Bool'
While-statement body should not be 'SELF_TYPE'
Cannot add expressions
Cannot subtract expressions
Cannot multiply expressions
Cannot divide expressions
Types cannot be compared with less-than-statement
Types cannot be compared with less-than-greater-than-statement
Types cannot be compared with equal-to-statement
Type must match void
Not-statement must be type 'Bool'
Negate-statement must be type 'Int'
Let binding identifier cannot be 'self'
Let assignment type mismatch
Object type cannot be assigned
Case expression type already exists
Case expression cannot be 'SELF_TYPE'
Case expressions empty
Identifier out of scope
Unknown expression type
Inheritence cycle
Class defined multiple times
Main class (Or inherited) missing main method
Main class does not exist
Type cannot be inherited from
Class cannot be inherited from as it does not exist
Attribute return type invalid
Method return type invalid
Method redefines inherited parameters
Method inherited parameters mismatch
main method should not have any parameters
Bad self dispatch arguments
Bad static dispatch arguments
Bad dynamic dispatch arguments
SELF TYPE improperly returned
Redeclared SELF TYPE













