Hunter Mast - PA6

Introduction:
	For PA6, the goal is to optimize my compiler from the previous project (PA5). My compiler does still seem to have some issues though. The main issues I believe lie with how the implementation map is created and then how dispatch is being done. Ignoring those, I had tried to add dead code elimination (DCE), constant propagation, assignment propagation, arithmetic reduction, and peephole optimization. I believe there are some issues with DCE in this case, so I tried to add DCE in another file called dce.py. In this file, we do DCE on a list of three address code instructions and removed any dead instructions. Below I will discuss all of the additions I made to my PA5 compiler to attempt to optimize it and then what I made for my dce.py file.

Dead Code Elimination:
	Starting out, I want to talk about my dce.py file. With this, I wanted to go through a file with TAC expressions and removed any that are deemed 'dead'. First, I started out by reading the file and using regular expressions to parse the file. The tokens that are in a TAC file are labels, returns, jumps, branches, integers, strings, Booleans, assignments, binary operators, unary operators, new objects, default objects, and method calls. After parsing all of this, we need to go through the main part of this file and do liveness analysis and dead code elimination.
	In liveness analysis, we our main goal is going through and making lists of what is live at each instruction. First, we go through branches and get all successors to each instruction. When jumping around, we need to know how important some of these jumps are and that we cannot remove the labels that populate from branching. We also need to know which instructions come before one each other and add check it later on. Then, we need to get all of the used and defined variables/registers for each instruction. With this information, we finally perform our actual liveness analysis. For liveness analysis, we need to do live_in = live_out + defined in a union together with used. Liveness analysis is performed backwards, so we reverse our list of instructions and start to get every set of live variables/registers in and out. We store the previous live_in and live_out to compare and see if any changes are being made and if not, then move on. If so, keep checking the one expression just in case there is a lot of changes needed. We return live_out and then move on to DCE itself. With DCE, there isn't much it has to do. It goes through and gets every variable defined and if it's in live_out, then add it to our optimized code. If it's a label, branch, jump, call, or return, then we do not change it. Something else we need to do here is check calls specifically. With calls, there are side effects if we remove any variables/registers that it relies on. To prevent this, we look for every call and add it to a list of instructions with said side effects. If there is a side effect, then we make sure that instruction is never removed. Live analysis is done again if our instructions are the same before and after analysis so we make sure our code is fully optimized. Afterwords, we just format the code back and print it out.
	This whole section shows DCE. Right now, this focuses on just the main method and ignores case instructions. Yet, it still shows how DCE is done overall. In my main compiler, I tried to add the same thing. It seems to remove too many instructions from the overall assembly output and change it slightly, but I am not sure if it is from my compiler overall, or DCE. I think the issues with DCE might be from dispatch in my compile, but I am not sure overall where it might come from. I did dce.py to make sure I had DCE in some way, which I believe I was able to create.

Constant Propagation:
	In my main compiler, I decided to do constant propagation, arithmetic reduction, and peephole reduction. Unlike my DCE and assignment propagation in my PA5 compiler, I believe all of these work very well. They are all separate functions with different goals, but very similar. Peephole optimization is very broad, so these may fall under that umbrella, but I wanted to focus on them separately. I may combine them after writing all of this into one peephole optimization function so we pass the AST once, but they are their own functions currently.
	With constant propagation, our goal is to combine constants and replace constants when possible in our AST. If we have 'x = 5 + 6', we could say that 5 + 6 is 11 and replace this with 'x = 11' to avoid doing more operations than we need to. Another part we try to do is replace any instance of that variable that is a constant with the constant itself to reduce variable assignments.
	Inside of my constant propagation, we need to consider not only each method, but attributes too. We first run through each attribute and combine them where we could and then move on to each method. By doing these operations directly before code generation, we are able to reduce lots of cycles from operations. Negation and making void checks just as 0 also helps a ton. There is not a lot of movement between functions with constant propagation, so this is a fairly simple process of just searching the AST for any constant and performing the operations.
	Something else I also added a bit later that cause a bit of issues is with mutable values. With while loops and other changes, we need to track and make sure they are not changing. I added to my deserialization section a part in assignment where there could be a value changing itself. In test3.cl, we have "result <- result + 1". This should not be replaced by a constant, so we make sure to check for that and prevent it.

Assignment Propagation:
	For assignment propagation, what I had tried to do was very similar process to constant propagation. We would want to reduce assignments of variables that we do not need to assign. If we perform 'x = y' and 'z = x', we could say 'z = y' and remove 'x' if there are no operations or changes to 'x'.
	For this, I had tried to go through and keep track of each variable that should actually not change at all. Doing this though, there were still a lot that change that shouldn't and no matter what I did, I could not figure out the right combination to work. This part is very similar to constant propagation, but also like DCE. I would have to keep track of what variables are live or dead and have important uses. Since I wasn't able to get that working within the scopes of my compiler, I ended up scrapping it all together. I did leave it in my code just like DCE if you would like to see what I had tried to do, but it overall did not really help me with anything.

Arithmetic Reduction:
	For arithmetic reduction, our goal is to reduce arithmetic operations that are ultimately useless. If we perform operations such as adding 0, subtracting 0, multiplying 1 or 0, or dividing by 1, we want to try and eliminate these operations. They all result in either 0 or no change in the variable, so we just leave it the same.
	Another operation we perform is with comparison operators. A lot of the time, this can be reduce to just true or false if we already have either constants with them or some other types. Just looking at true or false can lead to so much less operations and cycles. Of course, sometimes they can't be reduce, but we try to do it all when we can.
	This was all so similar to constant propagation that I ended up combining the both of them. Constant propagation also will make sure to reduce comparisons to Booleans and reduce some arithmetic operations like 'x + 0', for example. At this point, constant propagation is more of peephole optimization and is more doing constant folding and constant propagation, but I'm just going to simplify the name as a whole to constant propagation. This should speed up the compiler though as we do not need to go through the AST again.

Unboxing:
With unboxing, I don't really think it would have helped me a ton with my compiler for either reducing execution time or reducing cycles. In my compiler, I already set some values as unboxed and if they are unboxed, they are automatically set to the default value. There are not many times when I perform ‘new Int’ or something similar and when I do, my compiler wouldn’t really be doing all too much more. I did include it as a small section of my constant propagation where if I see ‘new Int’, ‘new String’, or ‘new Bool’, I would get it’s value and store it right away and remove the new aspect of it. It’s a small thing, but it is there if it were to ever come up. Most of my code is already not set up for that, so removing our unboxing would just meant that it would be harder for the rest of my compiler to recognize what is happening in my AST. It would require a lot more changes for minimal results.

Peephole Optimization:
	For peephole optimization itself, the function in my PA5 compiler has the goal of reducing all redundant pushes and pops in the code generated to COOL assembly. The way I attempted to reduce these is by having it look at each instruction and keep track of which registers are free and which are not. I know that it is suggested to do this with RegEx, but I thought it would be easier to check them with my classes. My classes directly say what registers are being stored and are keeping the strings that are printed, so we could use the variables from these classes to check registers.
	Going through it, we have 2 main goals. The first is removing excess pushes and pops and the second is reducing moves, stores, and loads. We set at the beginning that each register in COOL assembly is open (r0 through r8), along with 'fp' and 'ra'. Then, we go through each instruction and start to track which registers are being used. If one could be removed due to being redundant or not being necessary, we remove it and continue on. Once we go through all of this, we should have removed a lot of redundancy in our code generated.
	Currently, it doesn't really seem to be removing much, if anything. I am not exactly sure why, but it seems to mostly be looking if there are any pushes and pops directly next to each other that could be reduce. It doesn't seem to find any though. Theoretically, this should be removing any that it does come across. It might be that my compiler is not producing any, but it is hard to tell since my PA5 compiler is not working fully. I also wasn’t sure of any test cases I could make for this, so I did not mess with it too much. I did attempt to add it though.
	Something I had tried a few times, but was unable to add before finalizing this assignment is register optimization. Doing this, I would have hoped it would check each register and what is being stored inside of it. If it is redundant to store something that could be stored somewhere else directly so it isn't storing when using something right away or removing some of the registers that are not being utilized. We will see if I am able to make this part more in depth and a lot more complex, but for right now it is just looking for ones right next to each other.

test1.cl:
	For test1.cl, my goal was to focus on constant propagation and arithmetic reduction. There will be some dead code removed from this, but that is more of a goal in the next few test cases. As you can see in the file, there are lots of multiplying by 1, adding by 0, dividing by 1, etc. This of course is all to test for arithmetic reduction and show that these are being changed to either just the variable or something similar. Because of this, stuff like 'n <- m + 0' becomes 'n <- m', which can be removed. 'o <- n * 1', so 'n' could become 'm' here to reduce all of these operations. Eventually, DCE will remove 'n' for not being utilized, but again, that isn't what I was focusing on with this. There are also come constants that could be replaced like with 'x <- 5' and 'y <- x + 5'. This could just become 'y <- 5 + 5' and then 'y <- 10', which also could make it so that 'y = 10' becomes '10 = 10' and have arithmetic reduction also change '10 = 10' to just 'true'. With files like this, you can see how much it is reducing and how much it can optimize lots of arithmetic operations. At the bottom of this file, I included information on using profile with all of my optimizations. This does not include DCE though as I could not get it fully to work with my compiler.

test2.cl:
	For test2.cl, I wanted to focus overall on each kind of expression and with dead code elimination. Constant propagation and arithmetic reduction are used here, but they are not as important as dead code elimination in this section. I wanted something that could fully look at all of the dead code and show how this is operating on each kind of expression.
	There are 2 main ways of looking at this file. There is the way of making it a TAC file and running DCE on it and then running it right through my compiler without DCE. Either way, it does eliminate a lot of the dead code from this file. Every main expression in COOL is used here, so it covers a lot of bases. It is very good at for dce.py and comparing it to what optimized TAC code would be. TAC creation with the reference compiler only works if there is only the main method, so this should work well for it.

test3.cl:
	For test3.cl, I wanted to focus on how an actual file would be with multiple classes. test1.cl and test2.cl are of course testing for all of these certain conditions we implemented. In an actual file though, we may either not run into all of these conditions or have many different classes and methods. To test this, I used the test case from PA5 that I used for a similar idea.
	In this file, it first goes through and asks some questions about is 10 greater than 5 and calling a method to check that. It will then try to call some methods for copying values and resetting them. This is spread out between a Main class, class A, class NewTest, and class Expression. IO is inherited and there are multiple methods in each, resulting in a lot of dispatch and different values to be passed back and forth.
	In terms of my optimizations, we are not able to do DCE directly on it with dce.py. Because of the multiple classes, we cannot run it through using the TAC from the reference compiler. Using just the peephole optimizations I added like constant propagation, we seem to remove lots of the cycles. You can see below the reference compiler's profile compared to my PA5 compiler. Unfortanately, this test case can't be used with dce.py due to it having more than one class, but it should work great with constant propagation. I also included the results if we were to uncomment out DCE and assignment propagation from my PA5 compiler, but it doesn't work always for a lot of test cases.

test4.cl:
	For this final test, I mostly wanted to just show the speed at which constant propagation can be done over the unoptimzied reference compilers. With this test case, I have ever letter of the alphabet as a variable, along with a couple more. This should go through each of the attributes and continuously shrink them down until it ends with something much smaller and produces a smaller assembly code. Below I showed some of those results using 'profile'.
	With this test case, I also made a lot of these vairables dead. This way, we could also run dce.py and see in what ways this could optimize it. This test case is a fairly simple one, but I did want to create one with a lot of variables like this as a speed test. I would say that test3.cl is probably the hardest, but that is because of it's multiple classes and lots of dispatch.

Conclusion:
	After finishing all of these tests and optimizations, you can really see a lot of the ways I optimized the compiler. A majority of it seemed to be focusing on reducing cycles and cache misses. I originally tried to add at dataflow analysis into my compiler, but I realized that this actually would be a detriment to my PA5 compiler. In my compiler, I separate each line of the AST into an object called MethodImplementation. Since I am using the AST as my IR and not a control flow graph, there is no need for dataflow analysis. 
	Overall, I added quite a bit to my compiler to optimize cycles and the cache. A majority of the fixes and optimizations focus on peephole optimization with constant propagation and dead code elimination. While my dead code elimination wasn't fully working in my main compiler, I was able to get it working with the TAC instructions. I think my optimizations helped a lot overall with my compiler and 

test1.cl Profile with Reference Compiler:
Output: 05100105

PROFILE:           instructions =       1803 @    1 =>       1803
PROFILE:        pushes and pops =        404 @    1 =>        404
PROFILE:             cache hits =        618 @    0 =>          0
PROFILE:           cache misses =       1382 @  100 =>     138200
PROFILE:     branch predictions =         20 @    0 =>          0
PROFILE:  branch mispredictions =        131 @   20 =>       2620
PROFILE:        multiplications =          4 @   10 =>         40
PROFILE:              divisions =          2 @   40 =>         80
PROFILE:           system calls =          7 @ 1000 =>       7000
CYCLES: 150147

test1.cl Profile with My Compiler (Removing DCE and Arithmetic Propagation for Correct Output):
Output: 05100105

PROFILE:           instructions =       1167 @    1 =>       1167
PROFILE:        pushes and pops =        282 @    1 =>        282
PROFILE:             cache hits =        362 @    0 =>          0
PROFILE:           cache misses =       1051 @  100 =>     105100
PROFILE:     branch predictions =          6 @    0 =>          0
PROFILE:  branch mispredictions =         89 @   20 =>       1780
PROFILE:        multiplications =          0 @   10 =>          0
PROFILE:              divisions =          0 @   40 =>          0
PROFILE:           system calls =          7 @ 1000 =>       7000
CYCLES: 115329

test1.cl Profile with My Compiler (With DCE and Arithmetic Propagation):
Output:

PROFILE:           instructions =         34 @    1 =>         34
PROFILE:        pushes and pops =          8 @    1 =>          8
PROFILE:             cache hits =          4 @    0 =>          0
PROFILE:           cache misses =        530 @  100 =>      53000
PROFILE:     branch predictions =          0 @    0 =>          0
PROFILE:  branch mispredictions =          4 @   20 =>         80
PROFILE:        multiplications =          0 @   10 =>          0
PROFILE:              divisions =          0 @   40 =>          0
PROFILE:           system calls =          1 @ 1000 =>       1000
CYCLES: 54122

test2.cl Profile with Reference Compiler:
Output: x + y is not 25z > 10002

PROFILE:           instructions =       3920 @    1 =>       3920
PROFILE:        pushes and pops =        884 @    1 =>        884
PROFILE:             cache hits =       1240 @    0 =>          0
PROFILE:           cache misses =       2198 @  100 =>     219800
PROFILE:     branch predictions =         99 @    0 =>          0
PROFILE:  branch mispredictions =        282 @   20 =>       5640
PROFILE:        multiplications =          5 @   10 =>         50
PROFILE:              divisions =          1 @   40 =>         40
PROFILE:           system calls =          7 @ 1000 =>       7000
CYCLES: 237334

test2.cl Profile with My Compiler (Removing DCE and Arithmetic Propagation for Correct Output):
Output: x + y is not 25z > 10002

PROFILE:           instructions =       2684 @    1 =>       2684
PROFILE:        pushes and pops =        636 @    1 =>        636
PROFILE:             cache hits =        737 @    0 =>          0
PROFILE:           cache misses =       1995 @  100 =>     199500
PROFILE:     branch predictions =         76 @    0 =>          0
PROFILE:  branch mispredictions =        205 @   20 =>       4100
PROFILE:        multiplications =          1 @   10 =>         10
PROFILE:              divisions =          0 @   40 =>          0
PROFILE:           system calls =          7 @ 1000 =>       7000
CYCLES: 213930

test2.cl Profile with My Compiler With DCE and Arithmetic Propagation):
Output: x + y is not 25z > 10002

PROFILE:           instructions =       2600 @    1 =>       2600
PROFILE:        pushes and pops =        618 @    1 =>        618
PROFILE:             cache hits =        717 @    0 =>          0
PROFILE:           cache misses =       1928 @  100 =>     192800
PROFILE:     branch predictions =         76 @    0 =>          0
PROFILE:  branch mispredictions =        199 @   20 =>       3980
PROFILE:        multiplications =          1 @   10 =>         10
PROFILE:              divisions =          0 @   40 =>          0
PROFILE:           system calls =          7 @ 1000 =>       7000
CYCLES: 207008

test3.cl Profile with Reference Compiler:
*NOTE: Is 10 greater than 5? always came out wrong for my compiler, even without optimizing.

Output: 
Is 10 greater than 5?: False
Results: 15
reset_var:
Before reset: 0
After reset: 0

copy_var:

Original value: 10
Copied value: 42
Original value: 10


PROFILE:           instructions =       4246 @    1 =>       4246
PROFILE:        pushes and pops =       1099 @    1 =>       1099
PROFILE:             cache hits =       1595 @    0 =>          0
PROFILE:           cache misses =       2029 @  100 =>     202900
PROFILE:     branch predictions =        144 @    0 =>          0
PROFILE:  branch mispredictions =        326 @   20 =>       6520
PROFILE:        multiplications =          0 @   10 =>          0
PROFILE:              divisions =          0 @   40 =>          0
PROFILE:           system calls =         26 @ 1000 =>      26000
CYCLES: 240765

test3.cl Profile with My Compiler (Removing DCE and Arithmetic Propagation for Correct Output):
Output: 
Is 10 greater than 5?: True
Results: 15
reset_var:
Before reset: 0
After reset: 0

copy_var:

Original value: 10
Copied value: 42
Original value: 10


PROFILE:           instructions =       4246 @    1 =>       4246
PROFILE:        pushes and pops =       1099 @    1 =>       1099
PROFILE:             cache hits =       1578 @    0 =>          0
PROFILE:           cache misses =       1979 @  100 =>     197900
PROFILE:     branch predictions =        140 @    0 =>          0
PROFILE:  branch mispredictions =        327 @   20 =>       6540
PROFILE:        multiplications =          0 @   10 =>          0
PROFILE:              divisions =          0 @   40 =>          0
PROFILE:           system calls =         26 @ 1000 =>      26000
CYCLES: 235785

test3.cl Profile with My Compiler (With DCE and Arithmetic Propagation):
Output: Runs infinitely.

test4.cl Profile with Reference Compiler:
Output: 

PROFILE:           instructions =       7101 @    1 =>       7101
PROFILE:        pushes and pops =       1424 @    1 =>       1424
PROFILE:             cache hits =       2467 @    0 =>          0
PROFILE:           cache misses =       2974 @  100 =>     297400
PROFILE:     branch predictions =         94 @    0 =>          0
PROFILE:  branch mispredictions =        467 @   20 =>       9340
PROFILE:        multiplications =         14 @   10 =>        140
PROFILE:              divisions =          4 @   40 =>        160
PROFILE:           system calls =          1 @ 1000 =>       1000
CYCLES: 316565

test4.cl Profile with My Compiler (Removing DCE and Arithmetic Propagation for Correct Output):
Output: 

PROFILE:           instructions =       3989 @    1 =>       3989
PROFILE:        pushes and pops =        880 @    1 =>        880
PROFILE:             cache hits =       1173 @    0 =>          0
PROFILE:           cache misses =       1800 @  100 =>     180000
PROFILE:     branch predictions =         86 @    0 =>          0
PROFILE:  branch mispredictions =        282 @   20 =>       5640
PROFILE:        multiplications =          0 @   10 =>          0
PROFILE:              divisions =          0 @   40 =>          0
PROFILE:           system calls =          1 @ 1000 =>       1000
CYCLES: 191509

test4.cl Profile with My Compiler (With DCE and Arithmetic Propagation):
Output:

PROFILE:           instructions =       1690 @    1 =>       1690
PROFILE:        pushes and pops =        374 @    1 =>        374
PROFILE:             cache hits =        401 @    0 =>          0
PROFILE:           cache misses =       1336 @  100 =>     133600
PROFILE:     branch predictions =          0 @    0 =>          0
PROFILE:  branch mispredictions =        126 @   20 =>       2520
PROFILE:        multiplications =          0 @   10 =>          0
PROFILE:              divisions =          0 @   40 =>          0
PROFILE:           system calls =          1 @ 1000 =>       1000
CYCLES: 139184
