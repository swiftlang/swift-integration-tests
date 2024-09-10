import FoundationEssentials

#if canImport(FoundationMacros)
#error("Should not be able to import the FoundationMacros module directly")
#endif

let predicate = #Predicate<Int> {
	$0 > 2
}
print(predicate)
