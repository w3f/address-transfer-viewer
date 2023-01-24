# Address Transfer Viewer

Displays inbound and/or outbound transfers to an address, to some specififed degree. This will ONLY show addresses to which some DOT was transferred, not amount of DOT or number of transfers.

Note that you will need a Subscan API Key. To request one, see https://support.subscan.io/#introduction.

## Arguments

All arguments are mandatory.

### Argument Order

1. API Key - Your subscan API key. See https://support.subscan.io/#introduction
2. Degree - number of iterations (e.g. 1 = addresses that this address has transferred to, 2 = addresses that THOSE addresses have transferred to, etc.)
3. input/output/both - "input" for all transfers TO, "output" for all transfers FROM, "both" for both transfers TO and FROM. Case-insensitive.
4. Address - address to examine

## Examples

See all incoming transfers to some address.

```
% python viewer.py SUBSCAN_API_KEY 1 INPUT 15iZVdwdtXpn7Vx5SHW57pFSuazUEjLYcfL4NeSV4xNo3WPv

INCOMING TRANSFERS (DEGREE 1)
12pfPtoyeKRQRKJA1UwSYxSLoKa6AaZTR1V8YzTrUNAcrFZg
```

See all incoming and outgoing transfers to some address.

```
% python viewer.py SUBSCAN_API_KEY 1 BOTH 15iZVdwdtXpn7Vx5SHW57pFSuazUEjLYcfL4NeSV4xNo3WPv

INCOMING TRANSFERS (DEGREE 1)
12pfPtoyeKRQRKJA1UwSYxSLoKa6AaZTR1V8YzTrUNAcrFZg
OUTGOING TRANSFERS (DEGREE 1)
12pfPtoyeKRQRKJA1UwSYxSLoKa6AaZTR1V8YzTrUNAcrFZg
15dUAmZFm27mnhqdNRZmSnRWZcrNpmqbfSSJLnLiodCMeGzi
```

See all outgoing transfers from some address, and then all transfers from those "secondary" addresses.

```
 % python viewer.py SUBSCAN_API_KEY 2 OUTPUT 15iZVdwdtXpn7Vx5SHW57pFSuazUEjLYcfL4NeSV4xNo3WPv
OUTGOING TRANSFERS (DEGREE 1)
12pfPtoyeKRQRKJA1UwSYxSLoKa6AaZTR1V8YzTrUNAcrFZg
15dUAmZFm27mnhqdNRZmSnRWZcrNpmqbfSSJLnLiodCMeGzi

OUTGOING TRANSFERS (DEGREE 2)
12pfPtoyeKRQRKJA1UwSYxSLoKa6AaZTR1V8YzTrUNAcrFZg -> ['117ZPjxAoBNYd7GAiqU5kZaDN7N3rsMRKZzama3mr8sU93T', '12TYAV4ptHmwM1rf3isEy2a9QDmeLyy1JPSvqvqgLeXd82fS', '13fkMLZk2M1AwPM9JvWbQYDYQmkWyntR8bLFKrjZVMz1bnYz', '13wWr4ahKdc7HLpXSpuVdwKjKuLW9dcP4iaVLM2SZc3aX3aU', '14csKv3Y5YC54ZoVws1cgMPTtXxjDACrAa8xr7zEuVeaufZ2', '15JWX1964E5GG5yG3ZMNMdSMC4iU1AXxaBBEyzruzxGXChcH', '15iZVdwdtXpn7Vx5SHW57pFSuazUEjLYcfL4NeSV4xNo3WPv', '162JARMAK6XaSyHnyWrn8xDEAywffnDnEXvodLQnaRJFhFPh', '16851Ri3WDP9JPcSSuvp4JN2PZWtVNBRazm7TDLhhRjKvJtn', '16Sn4yLYC5TLSp6u5eXaURbtAjDWLeoacEjoSuZv4UyyrJaa']
15dUAmZFm27mnhqdNRZmSnRWZcrNpmqbfSSJLnLiodCMeGzi -> ['16Xuv8TZpqSP9iSxquSJ9CQDfnJink7tFFNg8YYLqE5DiXkn']
```