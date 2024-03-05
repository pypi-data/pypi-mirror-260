# atomicals
sebuah tutorial

khusus vps
1.
```
sudo apt-get update && sudo apt install git -y && sudo apt install apt-transport-https ca-certificates curl software-properties-common -y && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" && sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
```
2.

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
```

3 download file ini https://github.com/atomicals/atomicals-js 
lalu ekstrak di folder root vps mu

4 buka folder yg suda di ekstrak tadi 

```
cd atomical-js-master
```

5 build 

```
npm install
npm run build
```

6. buat wallet
```
yarn cli wallet-init
```

nanti akan mucul output seperti ini
>>>

Wallet created at wallet.json
phrase: maple maple maple maple maple maple maple maple maple maple maple maple
Legacy address (for change): 1FXL2CJ9nAC...u3e9Evdsa2pKrPhkag
Derive Path: m/86'/0'/0'/0/0
WIF: L5Sa65gNR6QsBjqK.....r6o4YzcqNRnJ1p4a6GPxqQQ
----------------------------------------------------

atau bisa langsung di akses di vps nya di wallet.json 
copy pharse nya masukin ke wallet atom ekstensi chrome
pastikan primary addresnya sama dg yg divps 

kalo sudah depo ke funding address

7. buat folder baru di root vps mu contohnya atommap

8. download file svg nya di https://github.com/Atombitworker/Atom-map/tree/main

   ekstrak file nya di pc mu
   jangan langsung di pindah smua ke vps soalnya bakalan lama

9 cari atom yg belum di mint di https://atomicalmarket.com/explorer

10. kalo dah nemu yg belum di claim misal (1001.atommap)
 tinggal cari di folder atoomap svg finall tadi cari 1001.avg lalu pindah ke folder atommap di vps mu tadi

11 
 ngemint
```
yarn cli mint-nft "/root/atommap/1001.atommap.svg" --satsbyte 30 --satsoutput 546 --bitworkc ab1001
```

1001.atommap.svg diganti dg yg mau lu mint
satsbyte buat atur gas
satsoutput biarin aja

bitworkc ganti dg nomer atoomap yg mau di mint 
misal mau mint 6969.atommap ganti jadi ab6969



