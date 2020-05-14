# maya_material_convert_tools
difference material convert~like arnold blin redshift~~

how to use?:
![image](https://github.com/qqqq88902494/maya_material_convert_tools/blob/master/GIF.gif )  

tips:
#by vfxmstc 
#email:410386656@qq.com
#maya2020
#tools_version:v01
#support:arnold to blin
#just select all materials and run it!
#you can change StartShader EndShader  or diff_color1  diff_color2  to other material,or wait for update~~~
#support mulity shadingengine,or tex or parm number connect，if error with RGB file, fix it:get old_shadingEnginefile color>.color.colorR

目前只有arnold 转blinn的功能  后续随缘完善~
急需用的也可以修改StartShader和EndShader  材质的类型名字,目前有判断是否一材质多物体使用，是否有链接贴图，否则获取数值，注意目前链接的贴图如果是RGB通道则可能会有问题 需要修改old_shadingEngine获取的.color为.color.colorR等，
和对应需要转换的参数名，比如高光也可以对应格式写下去。


