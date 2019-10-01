


alert("http://wwwtyro.github.io/cryptico/");

//Om ansluten: Ladda om sidan då och då eller iaf hämta ny information typ var 10 sekund

//interface för din egen session men som lagras på klienten
//användarnamn som är sökbart, ex telefonnummer och namn
//generera privat nyckel
//detta sparas i local storage så att det finns kvar nästa gång

//meddelanden laddas ner och finns kvar

//meddelanden kan skapas lokalt

//sök efter användare
// The passphrase used to repeatably generate this RSA key.
var Bits = 1024;
var PassPhrase1 = "The Moon is a Harsh Mistress.";
var PassPhrase2 = "There Ain't No Such Thing As A Free Lunch.";
// The length of the RSA key, in bits.
var PlainText = "Matt, I need you to help me with my Starcraft strategy.";

var MattsRSAkey = cryptico.generateRSAKey(PassPhrase1, Bits);
var SamsRSAkey = cryptico.generateRSAKey(PassPhrase2, Bits);

var MattsPublicKeyString = cryptico.publicKeyString(MattsRSAkey);


var EncryptionResult = cryptico.encrypt(PlainText, MattsPublicKeyString);

var DecryptionResult = cryptico.decrypt(CipherText, MattsRSAkey);


//Signing by Sams key!
var EncryptionResult = cryptico.encrypt(PlainText, MattsPublicKeyString, SamsRSAkey);
var PublicKeyID = cryptico.publicKeyID(EncryptionResult.publickey);