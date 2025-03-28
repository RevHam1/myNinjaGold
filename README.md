### Assignment: Ninja Gold Objectives:
*	Practice using session
	- Utilize session storing data on Backend then displaying that data for Front-End Interaction
*	Practice having the server use data sent by the client in a form
	- Utilize form data sending data from client to server
* Practice using hidden inputs
  - Utilize HTML hidden inputs to manage additional data in forms without affecting the user interface.

Create a simple game to test your understanding of flask, and implement the functionality below. For this assignment, you're going to create a mini-game that helps 
a ninja make some money! When you start the game, your ninja should have 0 gold. The ninja can go to different places (farm, cave, house, casino) and earn different 
amounts of gold. In the case of a casino, your ninja can earn or LOSE up to 50 golds. Your job is to create a web app that allows this ninja to earn gold and to 
display past activities of this ninja. Guidelines

*	Refer to the image below. (A picture of a Ninja is optional)
*	Have the four forms appear when the user goes to http://localhost:5000.
*	For the farm, your form would look something like
	- input type="hidden" name="building" value="farm" />
 * - input class="gold" type="submit" value="Find Gold!" />
*	In other words, you want to include a hidden value in the form and have each form submit the form information to /process_money.
* Have /process_money determine how much gold the user should have.
*	You should only have 2 routes -- '/' and '/process_money' (reset can be another route if you implement this feature).

![Image](https://github.com/user-attachments/assets/8ddd2133-83de-44f1-9deb-2cd88badfb58)
