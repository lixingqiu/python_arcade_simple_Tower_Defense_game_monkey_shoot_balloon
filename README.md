# python_arcade_simple_Tower_Defense_game_monkey_shoot_balloon
python arcade simple Tower Defense game monkey shoot_balloon
这是一个塔防类小游戏。本程序设计了半透明的圆形蔗罩mask，跟着拖曳的猴子移动。它的作用显示发射半径及提示不能在路径上放猴子。
发射原理是随机选择一只猴子,查找离它最近距离的泡泡。如果这个泡泡在发射半径，则计算方向向量，生成一枚子弹。
猴子是不能放在路径上的,如果靠得太近,则mask会切换造型进行提示,这时候松开鼠标指针是无法放置猴子。

操作方法：拖曳右上角的猴子，把它们放在离路径最近的地方。

本程序只是演示游戏基本原理，多关卡设计可以如下所示：
1、首先画好不同关卡的地图，画好后文件名为bg1.png,bg2.png,bg3.png.....
2、用程序“0_记录路径坐标.py”，加载不同的背景，自己拖曳鼠标指针，则会记录路径的坐标点，形成相应的path1.txt，path2.txt，path3.txt...
3、每关卡的泡泡数量不同，可以让泡泡数量随着关卡号的增加而增加，如建立self.pops_amount列表以记录每个关卡将会出现的泡泡数量。建立self.monkeys_amount列表存储每关可拖曳的猴子数量。
4、当有一个泡泡走完了整条路径，则表示防守失败。
5、当所有的泡泡被消灭，进入下一关，重新运行self.setup程序，加载新的path和背景等。
更多Python创意游戏请打开：http://www.lixingqiu.com


