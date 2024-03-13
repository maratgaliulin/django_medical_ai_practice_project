if(document.getElementById('pass_gen')){
    characters = Array.from('abcdefghijklmnopqrstuvwxyz');
    upper = Array.from('ABCDEFGHIJKLMNOPQRSTUVWXYZ');
    nums = Array.from('0123456789');
    spec = Array.from('!@#$%^&*()?><:;');
    length = document.getElementsByName('length')[0].value

    function removeElements(baseArr, mapArr){
        
        for (i = 0; i < baseArr.length; i++){
            for (j = 0; j < mapArr.length; j++){
                if(baseArr[i] === mapArr[j]){
                    baseArr.splice(i, 1);
                }
            }
        }
        return baseArr;
    }

    document.getElementsByName('length')[0].addEventListener('change', function(){
        length = this.value;
    })

    document.getElementsByName('uppercase')[0].addEventListener('change', function() {
        if(this.checked){
            Array.prototype.push.apply(characters, upper);
        } else{
            characters = removeElements(characters, upper)
        }
    })
        
    document.getElementsByName('numbers')[0].addEventListener('change', function() {
        if(this.checked){
            Array.prototype.push.apply(characters, nums);
        } else{
            characters = removeElements(characters, nums)
        }
    })

    document.getElementsByName('special')[0].addEventListener('change', function() {
        if(this.checked){
            Array.prototype.push.apply(characters, spec);
        } else{
            characters = removeElements(characters, spec)
        }
    })

    document.getElementById('pass_gen_btn').addEventListener('click', (e) => {
        function passwordGenerate(chars, lgth){
            var passw = ''
            for (x = 0; x < lgth; x++){
                passw += chars[Math.floor(Math.random() * chars.length)]
            }

            return passw
        }

        passw_final = passwordGenerate(characters, length)

        document.getElementById('pass_gen_result').innerHTML = passw_final
    })

}





// def password_gen(request):
//     characters = list()
//     if request.GET.get('uppercase'):
//         characters.extend(list())

//     if request.GET.get('numbers'):
//         characters.extend(list())

//     if request.GET.get('special'):
//         characters.extend(list())

//     length = int(request.GET.get('length'))

//     password = ''

//     for x in range(length):
//         password += random.choice(characters)

//     return render(request, CustomRegistrationView, {'password': password})