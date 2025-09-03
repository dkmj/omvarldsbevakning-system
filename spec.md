Nedan följer en sammanfattande specifikation baserad på alla krav och önskemål du beskrivit. Läs igenom och se om något saknas eller behöver förtydligas.

1. Översikt
	•	Mål: Bygga ett webbaserat system för omvärldsbevakning, där ett nätverk av experter bidrar med observationer. Dessa observationer samlas in per tidsperiod, sorteras och klustras under ett gemensamt möte, och mynnar ut i en rapport med tydliga kluster av relaterade observationer.

2. Roller och behörigheter
	1.	Bidragare (Expert)
	•	Kan lämna in observationer (inkl. rubrik, källa/fil, motivering).
	•	Ser och kan redigera sina egna bidrag.
	•	Kan radera eller begära radering av sina bidrag (kräver godkännande av admin).
	•	Kan lägga till och redigera taggar på egna bidrag.
	•	Har ingen tillgång till att klustrera observationer.
	2.	Databasadministratör
	•	Kan se alla inkomna observationer.
	•	Gör bedömning av spam/relevans och markerar observationer som “Godkänd”, “Osäker” eller “Radering”.
	•	Har tillgång till klustringsgränssnittet (färgkodning) under möten.
	•	Kan skapa rapporter när perioden är slut.
	3.	Superadministratör
	•	Kan skapa nya organisationer/”team” och lägga till användare i dem.
	•	Har full översikt över alla organisationers databaser och perioder.
	•	Sätter upp perioder på organisationsnivå (start- och slutdatum).
	•	Kan inte ändra bidragstexter (det görs på expert- eller admin-nivå).

3. Perioder och rapportering
	•	Periodstart: Bestäms av en superadmin för varje organisation.
	•	Bidragsfönster: Öppet till ett visst slutdatum. Under denna tid lämnar experter observationer.
	•	Efter slutdatum: Databasadministratören rensar och granskar observationerna, sätter status på ev. spam/outliers.
	•	Rapportgenerering: Systemet sammanställer en rapport över samtliga godkända observationer för perioden.
	•	Innehåller kluster (namn, beskrivning, robusthetsvärde 0–100) och de observationer som ingår i varje kluster.
	•	Arkiv: Rapporterna låses (t.ex. som pdf). Användare kan ladda ner historiska rapporter från ett arkiv via sitt gränssnitt.

4. Observationer
	•	Obligatoriska fält:
	1.	Dagens datum (förifyllt)
	2.	Expertens ID (förifyllt, via inloggning)
	3.	Rubrik
	4.	Länk eller fil (pdf, textfil, bild, max 25 MB)
	5.	Varför intressant? (fritext, 20–500 tecken)
	•	Valfria fält:
	•	Taggar (frivilligt): Systemet kan föreslå redan förekommande taggar i perioden.
	•	Lagring: All metadata + ev. bilaga lagras i databasen.
	•	Flera organisationer: Varje organisation har sin egen databas/tabellyta för observationer.

5. Klustring
	•	Grundprincip: Ett antal observationer samlas till ett kluster genom att de färgkodats lika.
	•	Gränssnitt:
	•	Alla observationer för perioden visas, går att scrolla eller bläddra.
	•	När en observation märks med en färg läggs den till ett kluster (eller flera om den har flera färger).
	•	Observationer kan vara helt utan färg om det beslutas.
	•	Flerfärgade observationer dyker upp under varje relevant kluster, med en indikation på att de också hör till andra kluster.
	•	Namn & motivering:
	•	Varje kluster får ett automatiskt “standardnamn” initialt.
	•	Människor i mötet måste ge klustret ett manuellt namn och kort motivering innan processen stängs.
	•	Ett “robusthetsvärde” (0–100) anger hur starkt gruppen anser att klustret hänger ihop.
	•	Samtidig användning:
	•	Flera databasadministratörer ska kunna arbeta i klustringsgränssnittet under mötet.
	•	Uppdateringar kan ske var 15:e/30:e sekund (eller liknande) – ingen realtidsdelning nödvändig, men rimlig autosync.
	•	Övriga användare (eller icke-inloggade deltagare) kan följa processen via en “tittvy”.
	•	Kommentarsfunktion:
	•	Vanliga användare ska kunna skicka in förslag till klustermotiveringar eller feedback.
	•	Förslagen är synliga för den som lämnat in förslaget och för databasadmin.
	•	Databasadmin väljer om förslaget ska användas/offentliggöras i klustermotiveringen.

6. Användarflöden (exempel)
	1.	Bidragare (Kalle) lägger till en observation
	1.	Kalle loggar in.
	2.	Fyller i rubrik, klistrar in länk eller laddar upp fil, skriver “varför intressant?” och ev. taggar.
	3.	Klickar “Skicka”. Observationen sparas i databasen.
	4.	Kalle ser en översikt av sina tidigare inlämningar denna period.
	2.	Databasadministratör
	1.	Loggar in.
	2.	Ser inkomna observationer. Markeras som “Godkänd”, “Osäker” eller “Radering”.
	3.	När perioden stänger, granskar återstående “Osäkra” för att avgöra status.
	4.	Skapar rapport genom att färgklustra observationer vid fysiskt/digitalt möte.
	5.	Namnger kluster, skriver sammanfattningar (ev. med hjälp av inkomna textförslag).
	6.	Genererar en låst slutrapport (pdf eller motsvarande).
	3.	Superadministratör
	1.	Kan lägga upp nya organisationer och bestämma perioder för dem.
	2.	Kan bjuda in användare till respektive organisation.
	3.	Har översikt över allt men ändrar inte enskilda observationstexter.

7. Sök- och filtrering
	•	Sökfunktion: Sök i titel, beskrivning, motivering, taggar, länkar.
	•	Tidsfilter: Visa enskilda observationer utifrån period(er), datumintervall.
	•	Taggar: Möjlighet att se eller filtrera på taggar, både inom och över perioder.

8. Loggning och historik
	•	Aktivitetslogg
	•	Tidsstämpel, användar-ID, typ av aktivitet (inloggning, inlämning, radering, klustring, rapportgenerering).
	•	Admin ska kunna se denna för att förstå hur systemet används.
	•	Rapportarkiv
	•	Varje period skapar en låst rapport (pdf).
	•	Tillgänglig för nerladdning på användarens egna sida (och i adminvy).
	•	Backup
	•	Regelbunden export av databasen för säkerhetskopiering.

9. Teknisk utformning (översikt)
	•	Webbaserad applikation:
	•	Möjlig att köra på en enkel hosting-tjänst inledningsvis.
	•	Ha möjligheten att flyttas till en arbetsplatsmiljö (t.ex. via container-lösning som Docker).
	•	Autentisering:
	•	Enkel inloggning med användarnamn och lösenord.
	•	Ingen tvåfaktorsautentisering i nuläget.
	•	HTTPS för säkrare överföring rekommenderas om det blir internet-exponering.
	•	Filer:
	•	Upp till ~25 MB per bilaga.
	•	Lagring i filsystem knutet till databasen eller i molnlagring beroende på behov.

10. Möjlig framtida utveckling
	•	Automatisk klustring/förslag: Möjligt i framtiden om man vill dra nytta av textanalys/AI.
	•	Djupare analys av källors återkommande.
	•	Tidslinje-/graf-visualisering: För att enklare se mönster över många perioder.
	•	Rollbaserad åtkomst i klustringsprocessen: Externa observatörer med begränsad vy.

Nästa steg
	1.	Granska och identifiera eventuella luckor: Känner du att något saknas i specifikationen?
	2.	Finjustera: Vi kan justera eller förtydliga baserat på dina kommentarer.
	3.	Utforma utvecklingsplan: När specifikationen känns komplett, kan den överlämnas till en utvecklare/team med en teknisk projektplan (val av ramverk, databas, tidsplan etc.).

Säg till om du ser något du vill förtydliga eller lägga till!