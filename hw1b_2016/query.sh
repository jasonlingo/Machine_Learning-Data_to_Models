printf "Question 1\n"
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=Yes
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=No

printf "\nQuestion 2\n"
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=Yes
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=No

printf "\nQuestion 3\n"
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=Yes,RoommateHasFlu=Yes

printf "\nQuestion 4\n"
# ./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=Yes,RoommateHasFlu=Yes FluRate=Severe
# ./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=Yes,RoommateHasFlu=Yes FluRate=Moderate
# ./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=Yes,RoommateHasFlu=Yes FluRate=Mild
./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=Yes FluRate=Severe
./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=Yes FluRate=Moderate
./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=Yes FluRate=Mild

./bayes-query network-extended.txt cpd-extended.txt RoommateHasFlu=Yes FluRate=Severe
./bayes-query network-extended.txt cpd-extended.txt RoommateHasFlu=Yes FluRate=Moderate
./bayes-query network-extended.txt cpd-extended.txt RoommateHasFlu=Yes FluRate=Mild

printf "\nQuestion 5\n"
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=Yes,CoworkerHasFlu=Yes
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=Yes,CoworkerHasFlu=Yes,FluRate=Mild
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=Yes,CoworkerHasFlu=Yes,FluRate=Moderate
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=Yes,CoworkerHasFlu=Yes,FluRate=Severe
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=No,CoworkerHasFlu=No
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=No,CoworkerHasFlu=No,FluRate=Mild
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=No,CoworkerHasFlu=No,FluRate=Moderate
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes RoommateHasFlu=No,CoworkerHasFlu=No,FluRate=Severe

printf "\nQuestion 6\n"
./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild IsFluSeason=No
./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate IsFluSeason=No
./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe IsFluSeason=No
./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Mild IsFluSeason=No
./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Moderate IsFluSeason=No
./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Severe IsFluSeason=No

./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate IsFluSeason=Yes
./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe IsFluSeason=Yes
./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild IsFluSeason=Yes
./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Moderate IsFluSeason=Yes
./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Severe IsFluSeason=Yes
./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Mild IsFluSeason=Yes

printf "\nQuestion 7\n"
./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Mild
./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Mild
./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Mild

./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Moderate
./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Moderate
./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Moderate

./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Severe
./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Severe
./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Severe

./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Mild,IsFluSeason=Yes
./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Mild,IsFluSeason=No
./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Mild,IsFluSeason=Yes
./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Mild,IsFluSeason=No
./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Mild,IsFluSeason=Yes
./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Mild,IsFluSeason=No


printf "\nQuestion 8\n"
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes MaryIsVaccinated=Yes
./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes MaryIsVaccinated=No



# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=No CoworkerHasFlu=Yes,RoommateHasFlu=Yes,MaryIsVaccinated=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=Yes,RoommateHasFlu=Yes,MaryIsVaccinated=No
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=No CoworkerHasFlu=Yes,RoommateHasFlu=Yes,MaryIsVaccinated=No 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=Yes,RoommateHasFlu=No,MaryIsVaccinated=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=No CoworkerHasFlu=Yes,RoommateHasFlu=No,MaryIsVaccinated=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=Yes,RoommateHasFlu=No,MaryIsVaccinated=No 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=No CoworkerHasFlu=Yes,RoommateHasFlu=No,MaryIsVaccinated=No 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=No,RoommateHasFlu=Yes,MaryIsVaccinated=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=No CoworkerHasFlu=No,RoommateHasFlu=Yes,MaryIsVaccinated=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=No,RoommateHasFlu=Yes,MaryIsVaccinated=No 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=No CoworkerHasFlu=No,RoommateHasFlu=Yes,MaryIsVaccinated=No 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=No,RoommateHasFlu=No,MaryIsVaccinated=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=No CoworkerHasFlu=No,RoommateHasFlu=No,MaryIsVaccinated=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=Yes CoworkerHasFlu=No,RoommateHasFlu=No,MaryIsVaccinated=No 
# ./bayes-query network-extended.txt cpd-extended.txt MaryGetsFlu=No CoworkerHasFlu=No,RoommateHasFlu=No,MaryIsVaccinated=No 
# ./bayes-query network-extended.txt cpd-extended.txt RoommateHasFlu=Yes FluRate=Mild 
# ./bayes-query network-extended.txt cpd-extended.txt RoommateHasFlu=No FluRate=Mild 
# ./bayes-query network-extended.txt cpd-extended.txt RoommateHasFlu=Yes FluRate=Moderate 
# ./bayes-query network-extended.txt cpd-extended.txt RoommateHasFlu=No FluRate=Moderate 
# ./bayes-query network-extended.txt cpd-extended.txt RoommateHasFlu=Yes FluRate=Severe 
# ./bayes-query network-extended.txt cpd-extended.txt RoommateHasFlu=No FluRate=Severe 
# ./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=Yes FluRate=Mild 
# ./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=No FluRate=Mild 
# ./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=Yes FluRate=Moderate 
# ./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=No FluRate=Moderate 
# ./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=Yes FluRate=Severe 
# ./bayes-query network-extended.txt cpd-extended.txt CoworkerHasFlu=No FluRate=Severe 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Mild,IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Mild,IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Mild,IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Moderate,IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Moderate,IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Moderate,IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Severe,IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Severe,IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Severe,IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Mild,IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Mild,IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Mild,IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Moderate,IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Moderate,IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Moderate,IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Mild PreviousFluRate=Severe,IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Moderate PreviousFluRate=Severe,IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt FluRate=Severe PreviousFluRate=Severe,IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Mild IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Moderate IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Severe IsFluSeason=Yes 
# ./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Mild IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Moderate IsFluSeason=No 
# ./bayes-query network-extended.txt cpd-extended.txt PreviousFluRate=Severe IsFluSeason=No 

